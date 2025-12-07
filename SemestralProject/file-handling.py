import json
import os

FILENAME = "savings_data.json"

# --- Basic Save/Load Functions ---
def save_data(data, filename=FILENAME):
    """Write the entire savings state into the JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print("Data saved!\n")

def load_data(filename=FILENAME):
    """Load saved data if file exists, otherwise return None."""
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as f:
        return json.load(f)