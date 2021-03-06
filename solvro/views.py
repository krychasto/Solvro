from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from links.models import Stops, Links


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for' + user)

                return redirect('login')

        context = {
            'form': form,
        }
        return render(request, 'solvro/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                messages.info(request, 'Username or password is incorrect')

        context = {}
        return render(request, 'solvro/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'solvro/homepage.html', context)

def create_database(request):
    Stops.objects.all().delete()
    Links.objects.all().delete()
    with open('solvro_city.json') as f:
        data = json.load(f)
    for stop in data['nodes']:
        created_stop_obj = Stops.objects.create(stop_id=stop['id'], stop_name=stop['stop_name'])
    stop_items = Stops.objects.all()

    for link in data['links']:
        created_link_obj = Links.objects.create(distance=link['distance'], source=Stops.objects.get(stop_id=link['source']).stop_name, target=Stops.objects.get(stop_id=link['target']).stop_name)
    link_items = Links.objects.all()
    context = {
        'stop_items': stop_items,
        'link_items': link_items,
    }
    return render(request, 'solvro/links.html', context)