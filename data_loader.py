import pandas as pd
import re
from .config import EXCEL_INPUT_FILE

def load_data():
    df = pd.read_excel(EXCEL_INPUT_FILE, sheet_name="Sheet1")

    rating_columns = [col for col in df.columns if col.startswith("How would you rate your connection with")]
    target_names = [re.sub(r"How would you rate your connection with ", "", col).strip("?") for col in rating_columns]

    strength_map = {
        "None": 0,
        "Weak": 1,
        "Strong": 2
    }

    edges = []
    for _, row in df.iterrows():
        source = row["Choose your name from the list below"]
        if pd.isna(source):
            continue
        for col, target in zip(rating_columns, target_names):
            rating = row[col]
            if isinstance(rating, str):
                rating_lower = rating.lower()
                if "weak" in rating_lower:
                    weight = strength_map["Weak"]
                elif "strong" in rating_lower:
                    weight = strength_map["Strong"]
                elif "none" in rating_lower:
                    weight = strength_map["None"]
                else:
                    continue
                edges.append({"Source": source, "Target": target, "Weight": weight})

    edges_df = pd.DataFrame(edges)

    # Build nodes with metadata
    all_names = set(edges_df["Source"]).union(set(edges_df["Target"]))
    nodes_df = pd.DataFrame({"Name": list(all_names)})

    attributes = df[[
        "Choose your name from the list below", 
        "Which office do you work from?",
        "Which Business Centre are you part of?",
        "Which of these communities do you feel part of?"
    ]].dropna()

    attributes.columns = ["Name", "Office", "Business_Centre", "Community"]

    from .config import ASIA_OFFICES
    attributes["Location"] = attributes["Office"].apply(lambda x: "Asia" if x in ASIA_OFFICES else x)
    nodes_df = nodes_df.merge(attributes, on="Name", how="left")

    return nodes_df, edges_df
