import json
import os

def load_or_create_json(filepath, default_data={}):
    # Check if the file exists
    if not os.path.exists(filepath):
        # If the file does not exist, write the default data to the file
        with open(filepath, 'w') as file:
            json.dump(default_data, file)
        return default_data
    else:
        # If the file exists, open it and load the JSON data
        with open(filepath, 'r') as file:
            return json.load(file)
    
