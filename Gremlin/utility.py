import json
import os
import textwrap

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
    

def show_help(help_map):
    longest_command_length = 0
    
    for command in help_map:
        command_length = len(command)
        if  command_length > longest_command_length:
            longest_command_length = command_length
            
    for command in sorted(help_map):
        text = f'\033[1m{command}\033[0m:{" " * (longest_command_length - len(command))} {help_map[command]}'
        colon_pos = text.find(':')
        formatted_text = textwrap.fill(text,
                                width=80,  # Maximum line width
                                subsequent_indent=' ' * (longest_command_length + 2))  # Indent for wrapped lines
        print(formatted_text)
        print()
