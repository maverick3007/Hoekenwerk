import networkx as nx
import matplotlib.pyplot as plt

# Maak een lege graaf
G = nx.Graph()

# Voeg in één actie knopen en bogen toe
G.add_weighted_edges_from([("A", "B", 6.0), ("A", "C", 5.0), ("A", "D", 4.0), ("D", "F", 4.0), ("D", "E", 4.0), ("F", "E", 3.0), ("F", "G", 2.0), ("F", "H", 7.0), ("H", "G", 6.0), ("G", "B", 5.0),("G", "E", 3.0), ("B", "C", 3.0), ("B", "E", 1.0), ("C", "D", 2.0)])

# Voeg een attribuut waarde toe en zet de waarde op 0 voor het startpunt en oneindig voor de andere
nx.set_node_attributes(G, float("inf"), "waarde")
nx.set_node_attributes(G, "", "komtvan")
nx.set_node_attributes(G, False, "bezocht")


# wandeling over alle punten volgens Dijkstra vertrekkende van een gegeven punt
def wandeling(start):
    # We zoeken het startpunt op
    startpunt = G.nodes[start]
    print(startpunt)
    # we zetten dat punt als bezocht
    startpunt["bezocht"]=True
    # We zoeken alle buren van dit punt op
    buren = G.neighbors(start)

    afstand_huidigeknoop = startpunt["waarde"]
    kleinste_afstand = float('inf')
    aantal_onbezochteburen = 0
    for buur in buren:
        buurnode = G.nodes[buur]
        bezocht = buurnode["bezocht"]

        if not bezocht:
            aantal_onbezochteburen += 1
            afstand = buurnode["waarde"]
            gewicht_verbinding = G.get_edge_data(start, buur)["weight"]
            kandidaat_afstand = afstand_huidigeknoop + gewicht_verbinding
            if kandidaat_afstand < afstand:
                buurnode['waarde'] = kandidaat_afstand
                buurnode["komtvan"] = start
            if kandidaat_afstand < kleinste_afstand:
                kleinste_afstand = kandidaat_afstand
                kandidaat_punt = buur
    if aantal_onbezochteburen > 0:
        wandeling(kandidaat_punt)

def dijkstra(start, eind):
    G.nodes[start]["waarde"] = 0
    wandeling(start)
    pad = []
    destnode = eind
    finished = False
    while not finished:
        pad.insert(0, destnode)
        previousNode = G.nodes[destnode]["komtvan"]

        if previousNode != "":
            destnode = previousNode
        else:
            finished = True
    print(pad)
    return pad

start = input("Geef startpunt: ")
eind = input("Geef eindpunt: ")

G.nodes[start]["waarde"] = 0
kortste_pad = dijkstra(start, eind)

counter = 0
nodecount = len(kortste_pad)

nx.set_edge_attributes(G, 'b', "color")
while counter < nodecount - 1:
    node = kortste_pad[counter]
    counter += 1
    nextnode = kortste_pad[counter]
    G.add_edge(node, nextnode, color='r')

labels = nx.get_edge_attributes(G,'weight')
colors = nx.get_edge_attributes(G,'color').values()
pos=nx.spring_layout(G, seed=5)
nx.draw(G, pos, with_labels=True, edge_color=colors)
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

plt.show()