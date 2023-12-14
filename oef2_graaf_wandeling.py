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


# wandeling over alle knopen volgens Dijkstra vertrekkende van een gegeven punt
def wandeling(start):
    # We zoeken de startknoop op
    startpunt = G.nodes[start]
    print(start, end = " ")
    print(startpunt)

    # we zetten die knoop als bezocht
    startpunt["bezocht"]=True
    # We zoeken alle buren van deze knoop op
    buren = G.neighbors(start)

    # we nemen de waarde van de startknoop
    afstand_huidigeknoop = startpunt["waarde"]
    kleinste_afstand = float('inf')
    aantal_onbezochteburen = 0
    for buur in buren:
        buurnode = G.nodes[buur]
        bezocht = buurnode["bezocht"]
        # Als de buur al bezocht is slaan we hem over
        if not bezocht:
            aantal_onbezochteburen += 1
            afstand = buurnode["waarde"]
            gewicht_verbinding = G.get_edge_data(start, buur)["weight"]
            # kandidaat_afstand is de mogelijk kortste afstand
            kandidaat_afstand = afstand_huidigeknoop + gewicht_verbinding
            if kandidaat_afstand < afstand:
                buurnode['waarde'] = kandidaat_afstand
                buurnode["komtvan"] = start
            if kandidaat_afstand < kleinste_afstand:
                kleinste_afstand = kandidaat_afstand
                kandidaat_punt = buur
    #als er nog onbezochte buren zijn doen we verder met een nieuwe knoop
    if aantal_onbezochteburen > 0:
        wandeling(kandidaat_punt)

start = input("Geef startpunt: ")
G.nodes[start]["waarde"] = 0
wandeling(start)