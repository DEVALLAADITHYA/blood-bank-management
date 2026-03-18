import json

def read_data(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return []

def write_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)
