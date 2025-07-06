import argparse
import os
from pathlib import Path
from .data_loader import load_data
from .network_builder import build_graph, mutual_strong_edges
from .reports.individual_report import generate_report

def cli():
    parser = argparse.ArgumentParser(description="Generate a social network report.")
    parser.add_argument("--file", required=True, help="Path to Excel file")
    parser.add_argument("--outdir", required=False, help="Optional output directory")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f" File not found: {args.file}")
        return

    nodes_df, edges_df = load_data(args.file)

    # Show names
    names = sorted(nodes_df["Name"].dropna().unique())
    print("\n Available Names:")
    for i, name in enumerate(names, 1):
        print(f"{i}. {name}")

    try:
        selected = int(input("\n Enter the number of the person to generate report for: "))
        if selected < 1 or selected > len(names):
            raise ValueError
    except ValueError:
        print(" Invalid selection.")
        return

    name = names[selected - 1]

    # Determine output directory
    if args.outdir:
        outdir = Path(args.outdir).expanduser()
    else:
        outdir = Path.home() / "Desktop"

    outdir.mkdir(parents=True, exist_ok=True)  # ensure it exists
    output_file = outdir / f"{name.replace(' ', '_')}_Network_Report.pdf"

    generate_report(name, edges_df, str(output_file))
    print(f"\n Report saved to: {output_file}")
    return str(output_file)
