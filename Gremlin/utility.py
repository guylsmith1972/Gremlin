from configuration import get_config
import json
import os
import re
import textwrap


def replace_commands(text):
    pattern = r'##(.*?)##'
    output = []
    last_end = 0

    for match in re.finditer(pattern, text):
        start, end = match.span()
        # Extract the match_value between ##
        match_value = match.group(1)
        # Get the transformed value
        transformed_value = get_command_name(match_value)
        # Append the text from the end of the last match to the start of the current match
        output.append(text[last_end:start])
        # Append the transformed value
        output.append(transformed_value)
        last_end = end  # Update last_end to the end of the current match

    # Append any remaining text after the last match
    output.append(text[last_end:])

    # Join all parts together to form the new text
    return ''.join(output)


def load_or_create_json(filepath, default_data):
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


def get_command_name(command_key):
    command_name = get_config(f'commands.builtins.{command_key}')[0]
    return command_name


def show_help(help_map):
    longest_command_length = 0
    
    for command in help_map:
        command_length = len(command)
        if  command_length > longest_command_length:
            longest_command_length = command_length
            
    for command in sorted(help_map):
        text = f'\033[1m{command}\033[0m:{" " * (longest_command_length - len(command))} {replace_commands(help_map[command])}'
        formatted_text = textwrap.fill(text,
                                width=80,  # Maximum line width
                                subsequent_indent=' ' * (longest_command_length + 2))  # Indent for wrapped lines
        print(formatted_text)
        print()
