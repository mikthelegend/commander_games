import json

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}