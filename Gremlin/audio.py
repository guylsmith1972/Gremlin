from configuration import get_config
from vosk import Model, KaldiRecognizer
import os
import pyaudio
import requests
import zipfile
from tqdm import tqdm  # tqdm is a library for a progress bar in the console


def download_file(url, filename):
    # Initial call to print 0% progress
    response = requests.get(url, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
    print("Download completed.")


def get_model():
    path = "./models/" + get_config('speech.model')

    if not os.path.exists(path):
        print(f"VOSK model not found at {path}. Starting download.")
        url = get_config('speech.default')
        print(f"Downloading the model from {url}...")
        zip_path = os.path.join('models', get_config('speech.model')) + '.zip'
        download_file(url, zip_path)
        # Unzip the file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('models')
            print("Model extracted successfully.")
    else:
        print(f"Model already exists at {path}.")
        
    return path

model_path = get_model()

# Initialize PyAudio
pa = pyaudio.PyAudio()

# Query the default input device information
default_device_index = pa.get_default_input_device_info()['index']
device_info = pa.get_device_info_by_index(default_device_index)

# Extract necessary device info
sample_rate = int(device_info['defaultSampleRate'])
channels = int(device_info['maxInputChannels'])
bit_depth = 16  # Assuming 16 bits per sample

# Set the correct PyAudio format based on the bit depth
if bit_depth == 16:
    audio_format = pyaudio.paInt16
elif bit_depth == 24:
    audio_format = pyaudio.paInt24
elif bit_depth == 32:
    audio_format = pyaudio.paInt32
else:
    raise ValueError("Unsupported bit depth")

# Frame size in bytes
frame_size = channels * (bit_depth // 8)

# Number of frames per buffer
sample_buffer_frames = 1024  # This is a reasonable number for many applications

# Calculate buffer size in bytes
sample_buffer_size = sample_buffer_frames * frame_size

print(f'Microphone sample rate: {sample_rate}')
print(f'Microphone channels: {channels}')
print(f'Frame size: {frame_size} bytes')
print(f'Sample buffer size: {sample_buffer_size} bytes')


def get_recognizer():
    # Load the model
    model = Model(model_path)

    p = pyaudio.PyAudio()
    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=sample_buffer_frames)
    stream.start_stream()

    # Initialize the recognizer
    recognizer = KaldiRecognizer(model, sample_rate)
    
    return stream, recognizer

    