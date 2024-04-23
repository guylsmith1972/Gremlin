from configuration import get_config
from pywinauto import Desktop, Application

import os
import psutil
import threading
import time

running_applications = []


def find_executables_in_path():
    executables = []
    # Get the PATH environment variable and split it into directories
    path_dirs = os.environ['PATH'].split(os.pathsep)

    for dir_path in path_dirs:
        # Check if the directory exists
        if os.path.isdir(dir_path):
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)

                # Check if the file is executable
                if os.name == 'nt':
                    # Windows: Check for executable extensions
                    if file_path.endswith(('.exe', '.bat', '.cmd')):
                        executables.append(file)
                else:
                    # Unix/Linux: Check if the file has execute permission
                    if os.access(file_path, os.X_OK) and os.path.isfile(file_path):
                        executables.append(file)

    return executables

available_executables = find_executables_in_path()


def find_apps(substring, applist):
    matches = []
    for entry in applist:
        if substring.lower() in entry.lower():
            matches.append(entry)
            
    return matches


def find_running_apps(substring):
    return find_apps(substring, [v[1] for v in running_applications])


def find_available_apps(substring):
    return find_apps(substring, available_executables)


def list_running_apps():
    for entry in running_applications:
        print(f'{entry[1]}: {entry[0]}')

        
def list_available_apps():
    for entry in sorted(available_executables):
        print(entry)


def update_running_applications():
    global running_applications
    while True:
        temp_list = []
        desktop = Desktop(backend="uia")
        for window in desktop.windows():
            try:
                # Check if the window is visible and has a title
                if window.is_visible() and window.window_text():
                    pid = window.process_id()
                    proc = psutil.Process(pid)
                    app_name = proc.name()
                    window_title = window.window_text()

                    # Add entries for both the application name and the window title
                    temp_list.append((pid, app_name))
                    temp_list.append((pid, window_title))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
            except Exception as e:
                print(f"Error checking window: {e}")

        running_applications = temp_list
        time.sleep(get_config('applications.monitoring.interval'))


def start_background_process_monitor():
    thread = threading.Thread(target=update_running_applications, daemon=True)
    thread.start()


def bring_app_to_foreground(app_name):
    app_name = app_name.lower()

    for pid, name in running_applications:
        print(f'looking for "{app_name}" in "{name.lower()}"')
        if app_name in name.lower():
            try:
                app = Application().connect(process=pid)
                app_window = app.top_window()
                app_window.set_focus()
                # app_window.move_window(x=0, y=0)
                print(f"Application with name '{app_name}' brought to foreground.")
                return
            except Exception as e:
                print(f"Error bringing application to foreground: {e}")

    print(f"No application or window found with name '{app_name}'")
