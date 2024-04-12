from ast import Interactive
import os
import textwrap
from configuration import get_config
import aliases
import applications
import pyautogui
import runtime
import subprocess
import utility


def list_items(transcript, args):
    mode = 'running'

    if args is not None and len(args) > 0:
        mode = args[0]

    if mode == 'running':   
        applications.list_running_apps()
    elif mode == 'available':
        applications.list_available_apps()
    elif mode == 'aliases':
        aliases.list()
    else:
        list_command = get_config('commands.builtins.list_items')
        print(f'Unknown argument "{mode}" for "{list_command}" command')

    
def resume_execution(transcript, args):
    print('Resuming command execution')
    runtime.set_mode('command')
    

def show_application(transcript, args):
    app_name = " ".join(args)
    applications.bring_app_to_foreground(app_name)


def suspend_execution(transcript, args):
    resume_command = get_config('commands.builtins.resume_execution')
    print(f'Suspending command execution except for "{resume_command}" command')
    runtime.set_mode('suspended')


def terminate(transcript, args):
    runtime.set_exit(True)


def create_alias(transcript, args):
    keyword = args[0]
    replacement = args[1:]
    aliases.add(keyword, ' '.join(replacement))

    
def web_search(transcript, args):
    query_string = f'https://www.google.com/search?q={"+".join(args)}'
    command = ['python', './commands/open.py', query_string]

    # Execute the file with the given command-line arguments
    subprocess.run(command)
    

def input_text(transcript, args):
    # Combine the array of strings into one single string with spaces
    input_text = ' '.join(args)
    
    # Type the combined string via the keyboard
    pyautogui.write(input_text)
    

def press_enter(transcript, args):
    pyautogui.write('\n')    
    

def interactive_mode(transcript, args):
    print(f"Entering interactive mode. Say {get_config('commands.builtins.command_mode')} or {get_config('commands.builtins.suspend_execution')} to switch to a different mode.")
    runtime.set_mode('interactive')

def command_mode(transcript, args):
    runtime.set_mode('command')
    

def get_help(transcript, args):
    list_builtins = True
    list_scripts = True
    list_specific = False
    
    if len(args) > 0:
        if args[0] == 'scripts':
            list_builtins = False
        elif args[0] == 'built-ins':
            list_scripts = False
        else:
            list_builtins = False
            list_scripts = False
            list_specific = True
            
    help_map = {}
        
    if list_builtins:
        for command in command_map:
            help_map[command] = command_map[command][1]
            
    if list_scripts:
        for root, dirs, files in os.walk(f'./{get_config("commands.directory")}'):
            for file in files:
                # Check if the file ends with the .py extension
                if file.endswith(".py"):
                    # Prepare the filename without extension and the full file path
                    filename = file[:-3]  # Removes the last 3 characters, which are '.py'
                    filepath = os.path.join(root, file)
                    
                    # Add to scripts
                    help_map[filename] = f'See comments in {filepath} for usage'

    if list_specific:
        print('\033[1mVerbose help not yet implemented.\033[0m')
        specific_command = args[0]
        filepath = os.path.join('commands', specific_command + '.py')
        if specific_command in command_map:
            help_map[specific_command] = command_map[specific_command][1]
        elif os.path.isfile(filepath):
            help_map[specific_command] = f'See comments in {filepath} for usage'

    utility.show_help(help_map)
        
    
command_map = {
     get_config('commands.builtins.command_mode')[0]: [command_mode, get_config('commands.builtins.command_mode')[1]],
     get_config('commands.builtins.create_alias')[0]: [create_alias, get_config('commands.builtins.create_alias')[1]],
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
