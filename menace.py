#!/usr/bin/env python3
"""Types a movie script line-by-line into the currently focused WhatsApp Web chat.

Windows build. A joke/copypasta tool -- use it only on chats where the other
person is in on the gag (see the responsible-use note in the README).

Run with:  python menace.py
"""

import os
import sys
import time
import webbrowser

import pyautogui

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Seconds to pause between messages. Keep this >= ~0.3s: WhatsApp Web will drop
# or throttle messages if you fire them too fast, and it keeps the kill-switch
# responsive.
DELAY_BETWEEN_LINES = 0.4

WEAPONS = {
    "bee": "bee.txt",
    "shrek": "shrek.txt",
    "sausage": "sausage.txt",
}

# Kill-switch: pyautogui's fail-safe. Slam the mouse pointer into ANY corner of
# the screen to abort (raises FailSafeException). No root and no extra library
# needed, unlike the `keyboard` module.
pyautogui.FAILSAFE = True

# On Windows pyautogui types into whatever window is focused -- including any
# browser -- so we just open WhatsApp Web in the default browser. (No XWayland
# workaround is needed here; that's only for Linux/Wayland.)


def open_whatsapp_web():
    """Open WhatsApp Web in the default browser."""
    webbrowser.open("https://web.whatsapp.com")


def spam(weapon_file):
    """Type every non-empty line of the given script file as a separate message."""
    path = os.path.join(SCRIPT_DIR, weapon_file)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            text = line.rstrip("\n")
            if not text.strip():
                continue  # don't send empty messages
            pyautogui.write(text)      # types the line (printable ASCII)
            pyautogui.press("enter")   # Enter sends it on WhatsApp Web
            time.sleep(DELAY_BETWEEN_LINES)


def main():
    weapon = input("Choose your weapon (bee/shrek/sausage): ").strip().lower()
    if weapon not in WEAPONS:
        print(f"Unknown weapon '{weapon}'. Pick one of: {', '.join(WEAPONS)}")
        sys.exit(1)

    print("\nOpening WhatsApp Web in your browser...")
    open_whatsapp_web()

    print(
        "\nNow, in the browser:\n"
        "  1. Log in (scan the QR code if it's your first time).\n"
        "  2. Click into the chat you want to send to, so the message box is focused.\n"
        "  3. Leave that browser window on top / focused.\n"
    )
    input("When the chat is open and focused, come back here and press Enter to start... ")

    print("\nStarting in 5 seconds -- click into the WhatsApp Web message box NOW.")
    print("(Kill-switch: throw the mouse into any corner of the screen to abort.)")
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)

    try:
        spam(WEAPONS[weapon])
    except pyautogui.FailSafeException:
        print("\nKill-switch triggered (mouse in a screen corner). Stopped.")
    except KeyboardInterrupt:
        print("\nStopped (Ctrl+C).")
    else:
        print("\nDone.")


if __name__ == "__main__":
    main()
