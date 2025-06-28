import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec, patches as mpatches
from textwrap import wrap
from ..config import ALIASES

def normalize(name):
    for key, values in ALIASES.items():
        if name in values:
            return key
    return name

def generate_report(name, edges_df, output_path):
    edges_df["Source"] = edges_df["Source"].apply(normalize)
    edges_df["Target"] = edges_df["Target"].apply(normalize)
    all_people = sorted(set(edges_df["Source"]).union(set(edges_df["Target"])))

    G = nx.DiGraph()
    for _, row in edges_df.iterrows():
        G.add_edge(row["Source"], row["Target"], weight=row["Weight"])

    ego_edges = [(u, v, d) for u, v, d in G.edges(data=True) if name in (u, v)]
    ego_graph = nx.DiGraph()
    ego_graph.add_edges_from(ego_edges)

    pos = nx.spring_layout(ego_graph, seed=42)
    node_sizes = [1200 if n == name else 400 for n in ego_graph.nodes()]
    node_colors = []

    for n in ego_graph.nodes():
        if n == name:
            node_colors.append("#FFD580")
        else:
            out = ego_graph[name][n]["weight"] if ego_graph.has_edge(name, n) else 0
            inc = ego_graph[n][name]["weight"] if ego_graph.has_edge(n, name) else 0
            if out == 2 and inc == 2:
                node_colors.append("#90EE90")
            elif out == 2 or inc == 2:
                node_colors.append("#ADD8E6")
            elif out == 1 and inc == 1:
                node_colors.append("#D8BFD8")
            else:
                node_colors.append("lightgray")

    categories = {
        "mutual_strong": [], "strong_weak": [], "strong_none": [],
        "weak_strong": [], "mutual_weak": [], "weak_none": [],
        "none_weak": [], "none_strong": [], "none_none": []
    }

    for other in all_people:
        if other == name:
            continue
        out = ego_graph[name][other]["weight"] if ego_graph.has_edge(name, other) else 0
        inc = ego_graph[other][name]["weight"] if ego_graph.has_edge(other, name) else 0

        if out == 2 and inc == 2:
            categories["mutual_strong"].append(other)
        elif out == 2 and inc == 1:
            categories["strong_weak"].append(other)
        elif out == 2 and inc == 0:
            categories["strong_none"].append(other)
        elif out == 1 and inc == 2:
            categories["weak_strong"].append(other)
        elif out == 1 and inc == 1:
            categories["mutual_weak"].append(other)
        elif out == 1 and inc == 0:
            categories["weak_none"].append(other)
        elif out == 0 and inc == 1:
            categories["none_weak"].append(other)
        elif out == 0 and inc == 2:
            categories["none_strong"].append(other)
        elif out == 0 and inc == 0:
            categories["none_none"].append(other)

    for key in categories:
        categories[key] = sorted(categories[key])

    feedback = [f"Hi {name},", "", "Here’s a quick look at your connection network:"]
    if categories["mutual_strong"]:
        feedback.append(f"[Mutual Strong] You and {len(categories['mutual_strong'])} others feel strongly connected.")
        feedback.append(f"Full list: {', '.join(categories['mutual_strong'])}")
    if categories["strong_weak"]:
        feedback.append(f"[Strong–Weak] You rated {len(categories['strong_weak'])} people strongly, but they rated you weaker.")
        feedback.append(f"Full list: {', '.join(categories['strong_weak'])}")
    if categories["strong_none"]:
        feedback.append(f"[Strong–No Response] You rated {len(categories['strong_none'])} people strongly, but they didn’t rate you.")
        feedback.append(f"Full list: {', '.join(categories['strong_none'])}")
    if categories["weak_strong"]:
        feedback.append(f"[Weak–Strong] You gave a weak rating to {len(categories['weak_strong'])} people, but they rated you strongly.")
        feedback.append(f"Full list: {', '.join(categories['weak_strong'])}")
    if categories["mutual_weak"]:
        feedback.append(f"[Mutual Weak] You and {len(categories['mutual_weak'])} others share a weak connection.")
        feedback.append(f"Full list: {', '.join(categories['mutual_weak'])}")
    if categories["weak_none"]:
        feedback.append(f"[Weak–No Response] You rated {len(categories['weak_none'])} people weakly, but they didn’t rate you.")
        feedback.append(f"Full list: {', '.join(categories['weak_none'])}")
    if categories["none_weak"]:
        feedback.append(f"[No Rating–Weak] {len(categories['none_weak'])} people rated you weakly, though you didn’t rate them.")
        feedback.append(f"Full list: {', '.join(categories['none_weak'])}")
    if categories["none_strong"]:
        feedback.append(f"[No Rating–Strong] {len(categories['none_strong'])} people rated you strongly, but you didn’t rate them.")
        feedback.append(f"Full list: {', '.join(categories['none_strong'])}")
    if categories["none_none"]:
        feedback.append(f"[No Exchange] You haven’t exchanged ratings with {len(categories['none_none'])} people.")
        feedback.append(f"Full list: {', '.join(categories['none_none'])}")

    feedback.append("Keep building — strong networks grow from clarity and conversation!")
    full_text = "\n".join(feedback)

    with PdfPages(output_path) as pdf:
        fig = plt.figure(figsize=(8.5, 11))
        spec = gridspec.GridSpec(2, 1, height_ratios=[4, 1])
        ax1 = fig.add_subplot(spec[0])
        ax1.set_title(f"Network Map: {name}", fontsize=16)
        ax1.axis("off")
        nx.draw_networkx_nodes(ego_graph, pos, node_size=node_sizes, node_color=node_colors, edgecolors='black', ax=ax1)
        for u, v, d in ego_graph.edges(data=True):
            if u == v: continue
            mutual = ego_graph.has_edge(v, u) and ego_graph[v][u]["weight"] == d["weight"]
            color, width = ('black', 3) if d["weight"] == 2 and mutual else ('gray', 2) if d["weight"] == 2 else ('lightgray', 1)
            nx.draw_networkx_edges(ego_graph, pos, edgelist=[(u, v)], width=width, edge_color=color, alpha=0.7, ax=ax1)

        ax2 = fig.add_subplot(spec[1])
        ax2.axis("off")
        legend = [
            mpatches.Patch(color="#FFD580", label="You"),
            mpatches.Patch(color="#90EE90", label="Mutual Strong"),
            mpatches.Patch(color="#ADD8E6", label="One-Way Strong"),
            mpatches.Patch(color="#D8BFD8", label="Mutual Weak"),
            mpatches.Patch(color="lightgray", label="One-Way Weak"),
        ]
        ax2.legend(handles=legend, loc="center", ncol=2, frameon=False, fontsize=10)
        pdf.savefig(fig)
        plt.close()

        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        ax.set_title(f"Feedback Summary: {name}", fontsize=16, loc="left", pad=20)
        y, spacing, max_width = 0.95, 0.045, 85
        for line in full_text.split('\n'):
            if not line.strip(): continue
            wrapped_lines = wrap(line, width=max_width)
            for text_line in wrapped_lines:
                ax.text(0.05, y, text_line, fontsize=10, ha="left")
                y -= spacing
                if y <= 0.05:
                    pdf.savefig(fig)
                    plt.close()
                    fig, ax = plt.subplots(figsize=(8.5, 11))
                    ax.axis("off")
                    y = 0.95
        pdf.savefig(fig)
        plt.close()
