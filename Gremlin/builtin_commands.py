import os
from configuration import get_config
import aliases
import applications
import pyautogui
import runtime
import subprocess
import utility


def create_alias(transcript, args):
    keyword = args[0]
    replacement = args[1:]
    aliases.add(keyword, ' '.join(replacement))

    
def command_mode(transcript, args):
    runtime.set_mode('command')
    

def delete_alias(transcript, args):
    aliases.remove(args[0])

    
def find_item(transcript, args):
    substring = ''.join(args)
    running_matches = applications.find_running_apps(substring)
    if len(running_matches) > 0:
        print(f'Currently running apps that match "{substring}"')
        for match in running_matches:
            print(match)
        print()
        
    available_matches = applications.find_available_apps(substring)
    if len(available_matches) > 0:
        print(f'Available apps that match "{substring}"')
        for match in available_matches:
            print(match)
    

def get_help(transcript, args):
    list_scripts = 1
    list_builtins = 2
    list_aliases = 4
    list_specific = 8
    list_type = list_scripts | list_builtins | list_aliases
    
    if len(args) > 0:
        if args[0] == 'scripts':
            list_type = list_scripts
        elif args[0] == 'built-ins':
            list_type = list_builtins
        elif args[0] == 'aliases':
            list_type = list_aliases
        else:
            list_type = list_specific
            
            
    help_map = {}
        
    if (list_type & list_builtins) == list_builtins:
        for command in command_map:
            help_map[command] = command_map[command][1]
            
    if (list_type & list_scripts) == list_scripts:
        for root, _, files in os.walk(f'{get_config("commands.directory")}'):
            for file in files:
                # Check if the file ends with the .py extension
                if file.endswith(".py"):
                    # Prepare the filename without extension and the full file path
                    filename = file[:-3]  # Removes the last 3 characters, which are '.py'
                    filepath = os.path.join(root, file)
                    
                    # Add to scripts
                    help_map[filename] = f'See comments in {filepath} for usage'
                    
    if (list_type & list_aliases) == list_aliases:
        all_aliases = aliases.get_all()
        for alias in all_aliases:
            help_map[alias] = f'alias for {all_aliases[alias]}'

    if (list_type & list_specific) == list_specific:
        print('\033[1mVerbose help not yet implemented.\033[0m')
        specific_command = args[0]
        filepath = os.path.join('commands', specific_command + '.py')
        if specific_command in command_map:
            help_map[specific_command] = command_map[specific_command][1]
        elif os.path.isfile(filepath):
            help_map[specific_command] = f'See comments in {filepath} for usage'

    utility.show_help(help_map)


def interactive_mode(transcript, args):
    print(f"Entering interactive mode. Say {get_config('commands.builtins.command_mode')[0]} or {get_config('commands.builtins.suspend_execution')[0]} to switch to a different mode.")
    runtime.set_mode('interactive')

        
def input_text(transcript, args):
    # Combine the array of strings into one single string with spaces
    text = ' '.join(args)
    
    # Type the combined string via the keyboard
    pyautogui.write(text)

    
def list_items(transcript, args):
    mode = 'running'

    if args is not None and len(args) > 0:
        mode = args[0]

    if mode == 'running':   
        applications.list_running_apps()
    elif mode == 'available':
        applications.list_available_apps()
    elif mode == 'aliases':
        aliases.print_to_console()
    else:
        list_command = get_config('commands.builtins.list_items')[0]
        print(f'Unknown argument "{mode}" for "{list_command}" command')


def press_enter(transcript, args):
    pyautogui.write('\n')    

    
def resume_execution(transcript, args):
    print('Resuming command execution')
    runtime.set_mode('command')


def show_application(transcript, args):
    app_name = " ".join(args)
    applications.bring_app_to_foreground(app_name)


def suspend_execution(transcript, args):
    resume_command = get_config('commands.builtins.resume_execution')[0]
    print(f'Suspending command execution except for "{resume_command}" command')
    runtime.set_mode('suspended')


def terminate(transcript, args):
    runtime.set_exit(True)
    
    
def web_search(transcript, args):
    query_string = f'https://www.google.com/search?q={"+".join(args)}'
    command = ['python', './commands/open.py', query_string]

    # Execute the file with the given command-line arguments
    subprocess.run(command)


command_map = {
     get_config('commands.builtins.command_mode')[0]: [command_mode, get_config('commands.builtins.command_mode')[1]],
     get_config('commands.builtins.create_alias')[0]: [create_alias, get_config('commands.builtins.create_alias')[1]],
     get_config('commands.builtins.delete_alias')[0]: [delete_alias, get_config('commands.builtins.delete_alias')[1]],
     get_config('commands.builtins.find_item')[0]: [find_item, get_config('commands.builtins.find_item')[1]],     
     get_config('commands.builtins.get_help')[0]: [get_help, get_config('commands.builtins.get_help')[1]],
     get_config('commands.builtins.input_text')[0]: [input_text, get_config('commands.builtins.input_text')[1]],
     get_config('commands.builtins.interactive_mode')[0]: [interactive_mode, get_config('commands.builtins.interactive_mode')[1]],
     get_config('commands.builtins.list_items')[0]: [list_items, get_config('commands.builtins.list_items')[1]],
     get_config('commands.builtins.create_alias')[0]: [create_alias, get_config('commands.builtins.create_alias')[1]],
     get_config('commands.builtins.press_enter')[0]: [press_enter, get_config('commands.builtins.press_enter')[1]],
     get_config('commands.builtins.resume_execution')[0]: [resume_execution, get_config('commands.builtins.resume_execution')[1]],
     get_config('commands.builtins.show_application')[0]: [show_application, get_config('commands.builtins.show_application')[1]],
     get_config('commands.builtins.suspend_execution')[0]: [suspend_execution, get_config('commands.builtins.suspend_execution')[1]],
     get_config('commands.builtins.terminate')[0]: [terminate, get_config('commands.builtins.terminate')[1]],
     get_config('commands.builtins.web_search')[0]: [web_search, get_config('commands.builtins.web_search')[1]],
}
