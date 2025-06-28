

import os
from .visualizations.draw_graph import draw_colored_network
from .reports.individual_report import generate_report  # Or batch generator
from .data_loader import load_data
from .network_builder import build_graph, mutual_strong_edges
from .reports.individual_report import generate_report

def main():
    # --- Get file path from user ---
    file_path = input("📄 Enter path to the Excel file (e.g., data.xlsx): ").strip().strip('"')
    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        return

    # Override file path in config dynamically
    from . import config
    config.EXCEL_INPUT_FILE = file_path

    # --- Load data ---
    nodes_df, edges_df = load_data()

    # Show available names
    print("\nAvailable names:")
    names = sorted(nodes_df["Name"].dropna().unique())
    for i, name in enumerate(names, 1):
        print(f"{i}. {name}")

    # --- Get target person from user ---
    choice = input("\n👤 Enter name or number to generate report for: ").strip()
    try:
        index = int(choice)
        person = names[index - 1]
    except:
        person = choice

    if person not in names:
        print(f"❌ Name '{person}' not found.")
        return

    # --- Generate report ---
    output_file = f"{person.replace(' ', '_')}_Network_Report.pdf"
    generate_report(person, edges_df, output_file)
    print(f"\n✅ Report generated: {output_file}")

if __name__ == "__main__":
    main()
