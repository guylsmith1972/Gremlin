must_exit = False    
mode = 'command'
valid_modes = ['command', 'interactive', 'suspended']


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
        print(f'invalid mode request: {new_mode}')


def get_mode():
    return mode


def is_mode_command(word):
    return word in valid_modes
