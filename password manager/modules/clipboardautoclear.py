import pyperclip
import time

def clear_clipboard():
    try:
        pyperclip.copy('')
        print("Clipboard cleared.")
    except Exception as e:
        print(f"Failed to clear clipboard: {e}")

def main():
    interval_seconds = 60*2 # 2 minutes
    while True:
        try:
            time.sleep(interval_seconds)
            clear_clipboard()
        except KeyboardInterrupt:
            print("Program terminated.")
            break
