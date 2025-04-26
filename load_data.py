import json

def load_data(filename):
    with open(filename) as f:
        data = json.load(f)
        return data['cuboids']