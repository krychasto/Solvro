"""This is module for generating Solvro City.
It generates the net of connections between stops
in Solvro City and the distances.
"""

import json
import random

import networkx as nx
# import matplotlib.pyplot as plt

from config import (
    FIRST_PARTS,
    SECOND_PARTS,
    STOPS_NUM,
    MAX_DISTANCE
)


def generate_stop_names(k=20):
    first_random = random.choices(FIRST_PARTS, k=k)
    second_random = random.choices(SECOND_PARTS, k=k)
    stop_names = [f"{first} {second}" for first, second in zip(first_random, second_random)]
    return stop_names


def generate_distances(city_plan):
    for edge in city_plan.edges():
        city_plan[edge[0]][edge[1]]['distance'] = random.randint(0, MAX_DISTANCE)


if __name__ == "__main__":
    city_plan = nx.gnp_random_graph(STOPS_NUM, 0.2)
    # uncomment if you want to draw it (tested only in jupyter notebook)
    # plt.subplot(121)
    # nx.draw(G, with_labels=True, font_weight='bold')

    # add names to stops
    stop_names = {i: f"Przystanek {stop_name}" for i, stop_name in enumerate(generate_stop_names(STOPS_NUM))}
    nx.set_node_attributes(city_plan, stop_names, 'stop_name')

    # add distances between stops
    generate_distances(city_plan)

    # write city to file
    with open("solvro_city.json", mode="w") as file:
        file.write(json.dumps(nx.node_link_data(city_plan), indent=4, sort_keys=True))