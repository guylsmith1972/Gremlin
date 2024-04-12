from configuration import get_config
import aliases
import applications
import audio
import builtin_commands
import json
import os
import runtime
import subprocess
import threading


command_prefix = get_config('commands.prefix')


def get_transcript(source, tag):
    as_json = json.loads(source)

    if tag in as_json:
        transcript = as_json[tag]
        if transcript is not None and len(transcript) > 0:
            return transcript

    return ''


def execute_file_with_args(filename, args, directory="."):
    # Construct the full path to the file
    filepath = os.path.join(directory, filename)

    # Check if the file exists in the given directory
    if os.path.isfile(filepath):
        # Construct the command to execute the file
        command = ['python', filepath] + args

        # Execute the file with the given command-line arguments
        subprocess.run(command)
    else:
        print(f"The file {filename} does not exist in the directory {directory}.")


def process_transcript(transcript):
    print('-' * 79)
    parts = transcript.split()
    alias = aliases.lookup(parts[0])
    if alias is not None:
        alias = alias.split() + parts[1:]
        print(f'Using alias "{parts[0]}" as command "{alias}"')
        parts = alias
        
    if len(parts) < 1 + (0 if command_prefix is None else 1):
        return
    
    if runtime.get_mode() == 'interactive' and not runtime.is_mode_command(parts[0]):
        args = parts
        command = 'input'
    else:
        args = parts[1:] if command_prefix is None else parts[2:]
        command = parts[0] if command_prefix is None else parts[1]
        
    if command_prefix is None or parts[0] == command_prefix:
        print(f'current mode: {runtime.get_mode()} and command is {command}')
        if runtime.get_mode() == "suspended" and command != get_config('commands.builtins.resume_execution'):
            resume_command = get_config("commands.builtins.resume_execution")
            print(f'Command execution is currently suspended. Say "{resume_command}" to resume command execution.')
        else:
            if command in builtin_commands.command_map:
                print(f'executing builtin command: {command} with arguments: {args}')
                print('-' * 79)
                builtin_commands.command_map[command][0](transcript, args)
            else:
                command += '.py'
                print(f'executing dynamic command: {command} with arguments: {args}')
                print('-' * 79)
                execute_file_with_args(command, args, f'./{get_config("commands.directory")}')


def start_process_transcript_thread(transcript):
    # Create a Thread object targeting the process_transcript function with the transcript as an argument
    thread = threading.Thread(target=process_transcript, args=(transcript,))
    # Start the thread
    thread.start()


def main():
    # Start the background process monitor
    applications.start_background_process_monitor()

    # Initialize the recognizer
    stream, recognizer = audio.get_recognizer()

    print(f"Listening. Say \"{get_config('commands.builtins.get_help')[0]}\" to get a listing of available voice commands.")

    # Process audio in real-time and handle the transcript
    while not runtime.get_exit():
        data = stream.read(audio.sample_buffer_size)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            transcript = get_transcript(result, 'text')
            if transcript is not None and len(transcript) > 0:
                print(transcript)
                start_process_transcript_thread(transcript)


if __name__ == '__main__':
    main()
