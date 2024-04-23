from configuration import get_config
from pywinauto import Desktop, Application
from transcriber import Transcriber
import applications
import runtime
import threading


def start_process_transcript_thread(transcript):
    # Create a Thread object targeting the process_transcript function with the transcript as an argument
    thread = threading.Thread(target=runtime.current_mode, args=(transcript,))
    # Start the thread
    thread.start()


def main():
    # Start the background process monitor
    applications.start_background_process_monitor()

    transcriber = Transcriber()
    
    print(f"Listening. Say \"{get_config('commands.builtins.get_help')[0]}\" to get a listing of available voice commands.")

    # Process audio in real-time and handle the transcript
    while not runtime.get_exit():
        extended, transcript = transcriber.extend()
        if extended:
            print(transcript)
            start_process_transcript_thread(transcript)


if __name__ == '__main__':
    main()
