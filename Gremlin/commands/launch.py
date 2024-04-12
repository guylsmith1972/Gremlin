import sys
import subprocess

def launch_application():
    # Split the command-line arguments into parts
    parts = sys.argv[1:]

    # Join the parts to form the application name
    app_name = "".join(parts)

    # Run the app
    subprocess.run([app_name])
    

if __name__ == "__main__":
    launch_application()
