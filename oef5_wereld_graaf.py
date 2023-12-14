import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import random
from math import radians, sin, cos, sqrt, atan2



def haversine_distance(node1, node2):
    lat1 = node1['lat']/10000
    lat2 = node2['lat']/10000
    lon1 = node1['lng']/10000
    lon2 = node2['lng']/10000
    # Straal aarde kilometers
    R = 6371.0

    # Convert breedtegraad en lengtegraad in radialen
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Bereken het verschil in coördinaten
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formule voor afstandsberekening
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # afstand in kilometers met schaalparameter
    distance = R * c

    return distance

# opstellen graaf knopen
G = nx.Graph()
df = pd.read_csv("fullcities.csv", sep=';', encoding='latin-1')
test = df.keys()
for ind in df.index:
    if df['country'][ind] == 'Belgium' and  df['population'][ind] > 20000:
        G.add_node(df['city_ascii'][ind], pos=(df['lng'][ind], df['lat'][ind] ), lat=df['lat'][ind], lng=df['lng'][ind])
dict(G.nodes(default=1))

for node in G.nodes:
    radius = 10
    roadcounter = 0
    while roadcounter < 3:
        for node2 in G.nodes:
            if node != node2:
                start = G.nodes[node]
                eind = G.nodes[node2]
                dist = haversine_distance(start, eind)

                if dist < radius:
                    dist = float(dist)
                    dist = round(dist, 1)
                    G.add_weighted_edges_from([(node, node2, dist)])
                    roadcounter += 1
        radius += 5


start = input("Geef startpunt: ")
eind = input("Geef eindpunt: ")
pad = nx.dijkstra_path(G, start, eind, weight='weight')
print(pad)

# tonen graaf
counter = 0
nodecount = len(pad)

nx.set_edge_attributes(G, 'b', "color")
while counter < nodecount - 1:
    node = pad[counter]
    counter += 1
    nextnode = pad[counter]
    G.add_edge(node, nextnode, color='r')

pos = nx.get_node_attributes(G, 'pos')
labels = nx.get_edge_attributes(G,'weight')
colors = nx.get_edge_attributes(G,'color').values()
nx.draw(G, pos, with_labels=True, edge_color=colors)
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)


plt.show()

