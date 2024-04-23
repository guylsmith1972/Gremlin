from configuration import get_config
import mode_chatter
import mode_command
import mode_interactive
import mode_suspended


must_exit = False

current_mode = mode_command.process_transcript

modes = {
    get_config('commands.builtins.chatter_mode')[0]: mode_chatter.process_transcript,
    get_config('commands.builtins.command_mode')[0]: mode_command.process_transcript,
    get_config('commands.builtins.interactive_mode')[0]:  mode_interactive.process_transcript,
    get_config('commands.builtins.resume_execution')[0]: mode_command.process_transcript,
    get_config('commands.builtins.suspend_execution')[0]: mode_suspended.process_transcript
}

command_prefix = get_config('commands.prefix')


def set_exit(flag):
    global must_exit
    must_exit = flag


def get_exit():
    return must_exit


def set_mode(new_mode):
    if new_mode in modes:
        global current_mode
        current_mode = modes[new_mode]
    else:
        print(f"invalid mode request: {new_mode}")


def is_modeswitch(command):
    return command in modes
