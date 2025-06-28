import networkx as nx

def build_graph(edges_df):
    G = nx.DiGraph()
    for _, row in edges_df.iterrows():
        G.add_edge(row["Source"], row["Target"], weight=row["Weight"])
    return G

def mutual_strong_edges(G):
    mutual = set()
    for u, v, data in G.edges(data=True):
        if data['weight'] == 2 and G.has_edge(v, u) and G[v][u]['weight'] == 2:
            mutual.add((u, v))
            mutual.add((v, u))
    return mutual
