import requests
import subprocess


def query_llm(prompt):
    url = 'http://localhost:11434/api/generate'
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['response']
    except requests.RequestException as e:
        return {"error": str(e)}


def start_llama_server():
    global llama_process
    # Start the llama server as a background process
    llama_process = subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def stop_llama_server():
    if llama_process:
        llama_process.terminate()  # Terminate the subprocess
        llama_process.wait()       # Wait for the process to terminate
