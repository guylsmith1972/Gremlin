from ast import Interactive
from configuration import get_config
import aliases
import applications
import pyautogui
import runtime
import subprocess


def list_applications(transcript, args):
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
        list_command = get_config('commands.builtins.list_applications')
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
    for command in command_map:
        print(command)
        

    
command_map = {
     get_config('commands.builtins.command_mode'): command_mode,
     get_config('commands.builtins.create_alias'): create_alias,
     get_config('commands.builtins.get_help'): get_help,
     get_config('commands.builtins.input_text'): input_text,
     get_config('commands.builtins.interactive_mode'): interactive_mode,
     get_config('commands.builtins.list_applications'): list_applications,
     get_config('commands.builtins.create_alias'): create_alias,
     get_config('commands.builtins.press_enter'): press_enter,
     get_config('commands.builtins.resume_execution'): resume_execution,
     get_config('commands.builtins.show_application'): show_application,
     get_config('commands.builtins.suspend_execution'): suspend_execution,
     get_config('commands.builtins.terminate'): terminate,
     get_config('commands.builtins.web_search'): web_search
}
