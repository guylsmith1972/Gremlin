from configuration import get_config
import aliases
import builtin_commands
import os
import runtime
import subprocess


def execute_file_with_args(filename, args, directory="."):
    # Construct the full path to the file
    filepath = os.path.join(directory, filename)

    # Check if the file exists in the given directory
    if os.path.isfile(filepath):
        # Construct the command to execute the file
        command = ['python', filepath] + args

        # Execute the file with the given command-line arguments
        subprocess.run(command)
        return True
    else:
        print(f"The file {filename} does not exist in the directory {directory}.")
        return False


def parse(full_transcript):
    transcript = full_transcript[-1]
    parts = transcript.split()
    alias = aliases.lookup(parts[0])
    if alias is not None:
        alias = alias.split() + parts[1:]
        print(f'Using alias "{parts[0]}" as command "{alias}"')
        parts = alias
        transcript = ' '.join(parts)
        
    return transcript, parts


def execute(transcript, command, args, modeswitch_only=False):
    if modeswitch_only:
        if runtime.is_modeswitch(command):
            print(f'Executing modeswitch command {command}')
            print('-' * 79)
            builtin_commands.command_map[command][0](transcript, args)
            return True
    else:
        if command in builtin_commands.command_map:
            print(f'executing builtin command: {command} with arguments: {args}')
            print('-' * 79)
            builtin_commands.command_map[command][0](transcript, args)
            return True
        else:
            command += '.py'
            print(f'executing dynamic command: {command} with arguments: {args}')
            print('-' * 79)
            return execute_file_with_args(command, args, f'./{get_config("commands.directory")}')                    
