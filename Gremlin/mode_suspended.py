from configuration import get_config
import command_handler
import runtime


def process_transcript(full_transcript):
    transcript, parts = command_handler.parse(full_transcript)
       
    if len(parts) < 1 + (0 if runtime.command_prefix is None else 1):
        return
    
    args = parts[1:] if runtime.command_prefix is None else parts[2:]
    command = parts[0] if runtime.command_prefix is None else parts[1]
        
    if runtime.command_prefix is None or parts[0] == runtime.command_prefix:
        command_handler.execute(transcript, command, args, modeswitch_only=True)
