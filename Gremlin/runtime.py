from configuration import get_config


must_exit = False
mode = "command"
valid_modes = ["command", "interactive", "suspended"]
mode_commands = [
    get_config("commands.builtins.command_mode")[0],
    get_config("commands.builtins.interactive_mode")[0],
    get_config("commands.builtins.resume_execution")[0],
    get_config("commands.builtins.suspend_execution")[0],
]


def set_exit(flag):
    global must_exit
    must_exit = flag


def get_exit():
    return must_exit


def set_mode(new_mode):
    if new_mode in valid_modes:
        global mode
        mode = new_mode
    else:
        print(f"invalid mode request: {new_mode}")


def get_mode():
    return mode


def is_mode_command(word):
    return word in mode_commands
