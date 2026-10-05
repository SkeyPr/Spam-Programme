#!/usr/bin/env python3
"""Types a movie script line-by-line into the currently focused WhatsApp Web chat.

A joke/copypasta tool. Use it only on chats where the other person is in on
the gag -- see the responsible-use note in the README.
"""

import os
import shutil
import subprocess
import sys
import time

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

# Kill-switch: pyautogui's fail-safe. Slam the mouse pointer into the TOP-LEFT
# corner of the screen at any time to abort (raises FailSafeException). No root
# and no extra library needed, unlike the `keyboard` module.
pyautogui.FAILSAFE = True

# --- Wayland note -----------------------------------------------------------
# pyautogui types via XTEST, which only reaches X11 / XWayland windows. On a
# Wayland session (GNOME, etc.) the default/snap browser usually runs as a
# NATIVE Wayland client and receives NOTHING. So we launch Chromium forced into
# X11 mode (--ozone-platform=x11) with its own profile; that window DOES receive
# the keystrokes. (Verified on this machine.)
CHROMIUM_X11_PROFILE = os.path.expanduser("~/snap/chromium/common/menace-profile")


def find_chromium():
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        path = shutil.which(name)
        if path:
            return path
    return None


def open_whatsapp_web():
    """Open WhatsApp Web in Chromium forced to X11 so pyautogui can type into it."""
    chromium = find_chromium()
    if not chromium:
        print("Chromium/Chrome not found. Install it, or open any X11/XWayland")
        print("browser at https://web.whatsapp.com yourself, then continue.")
        return
    subprocess.Popen(
        [chromium, "--ozone-platform=x11",
         f"--user-data-dir={CHROMIUM_X11_PROFILE}",
         "--no-first-run", "https://web.whatsapp.com"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


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

    print("\nOpening WhatsApp Web in Chromium (X11 mode)...")
    open_whatsapp_web()

    print(
        "\nNow, in the Chromium window that just opened:\n"
        "  1. Log in (scan the QR code -- first time only; the profile is saved).\n"
        "  2. Click into the chat you want to send to, so the message box is focused.\n"
        "  3. Leave that Chromium window on top / focused.\n"
        "  (Use THIS Chromium window -- not Firefox/your normal browser, or the\n"
        "   keystrokes won't land.)\n"
    )
    input("When the chat is open and focused, come back here and press Enter to start... ")

    print("\nStarting in 5 seconds -- click into the WhatsApp Web message box NOW.")
    print("(Kill-switch: throw the mouse into the top-left screen corner to abort.)")
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)

    try:
        spam(WEAPONS[weapon])
    except pyautogui.FailSafeException:
        print("\nKill-switch triggered (mouse in top-left corner). Stopped.")
    except KeyboardInterrupt:
        print("\nStopped (Ctrl+C).")
    else:
        print("\nDone.")


if __name__ == "__main__":
    main()
