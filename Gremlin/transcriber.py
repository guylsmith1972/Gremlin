import audio
import json

class Transcriber:
    """Handles the transcription of audio streams using a given recognizer.
    Ensures that only one instance handles the microphone input.
    """
    
    _instance = None  # Singleton instance holder

    def __new__(cls):
        """Ensure only one instance of Transcriber is created."""
        if cls._instance is None:
            cls._instance = super(Transcriber, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the transcriber with a recognizer and an empty transcript."""
        if not self._initialized:
            self.full_transcript = []
            try:
                self.stream, self.recognizer = audio.get_recognizer()
                self._initialized = True
            except Exception as e:
                # Handle initialization errors
                print(f"Failed to initialize the recognizer: {e}")
                self.stream = self.recognizer = None

    def clear(self):
        """Clear the current transcript."""
        self.full_transcript = []

    def get_transcript(self):
        """Return the current full transcript."""
        return self.full_transcript

    def extend(self):
        """Extend the transcript with newly recognized audio data."""
        if self.stream is None or self.recognizer is None:
            return False, self.full_transcript
        
        extended = False
        try:
            data = self.stream.read(audio.sample_buffer_size)
            if self.recognizer.AcceptWaveform(data):
                result = self.recognizer.Result()
                as_json = json.loads(result)
                transcript = as_json.get("text", "")
                if transcript:
                    self.full_transcript.append(transcript)
                    extended = True
        except Exception as e:
            print(f"Error during transcription: {e}")
        
        return extended, self.full_transcript
