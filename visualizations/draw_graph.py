import networkx as nx
import matplotlib.pyplot as plt

def draw_colored_network(G, pos, node_colors, mutual_edges):
    plt.figure(figsize=(14, 10))
    nx.draw_networkx_nodes(G, pos, node_size=400, node_color=node_colors, edgecolors='black')
    for u, v, data in G.edges(data=True):
        weight = data['weight']
        if (u, v) in mutual_edges:
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=3, edge_color='black')
        elif weight == 2:
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=2, edge_color='gray')
        elif weight == 1:
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=1, edge_color='lightgray')
    plt.title("Network Graph")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
