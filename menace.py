#importing all necessary libraries

import pyautogui  
import time
import os
import keyboard

time.sleep(5)

killswitch_triggered = False

#defining functions for each movie script spamming

def bee():
    with open("bee.txt", "r") as f:
        for word in f:
            if killswitch_triggered:
                return
            pyautogui.typewrite(word)
            pyautogui.press("enter")


def shrek():
    with open("shrek.txt", "r") as f:
        for word in f:
            if killswitch_triggered:
                return
            pyautogui.typewrite(word)
            pyautogui.press("enter")
            time.sleep(0)


def sausage():
    with open("sausage.txt", "r") as f:
        for word in f:
            if killswitch_triggered:
                return
            pyautogui.typewrite(word)
            pyautogui.press("enter")
            time.sleep(0)


def killswitch_callback(event):
    global killswitch_triggered
    killswitch_triggered = True


# Register the key combination Ctrl + Esc for killswitch
keyboard.add_hotkey("Ctrl + Esc", killswitch_callback)

app = input("Whatsapp or discord? \n")

#Part of the programme that helps us in spamming on whatsapp

if app == "whatsapp":
    bruh = input("who/what do you want to spam: ")
    ayo = input("Choose your weapon (bee/shrek/sausage): ")

    whatsapp_path = r"ThePathToWhatsapp" #Enter here the path to your whatsapp desktop application
    os.startfile(whatsapp_path)
    time.sleep(10)
    pyautogui.typewrite(bruh)
    pyautogui.press("down")
    pyautogui.press("enter")
    time.sleep(8)

    if ayo == "bee":
        bee()
    elif ayo == "shrek":
        shrek()
    elif ayo == "sausage":
        sausage()

# The part of the programme that will help in spamming on discord! (via your browser)

elif app == "discord":
    bruhh = input("who/what do you want to spam: ")
    ayoo = input("Choose your weapon (bee/shrek/sausage): ")

    if bruhh == "enterprompt":                                #Enter the pre-set prompt that you want to type a particular person on discord
        promptlink = "enteryourlink"                          #Enter the link of the person's dm 
        os.startfile(promptlink)                              #You can add more prompts of your own to type in your friends' dms
        if ayoo == "bee":
            bee()
        elif ayoo == "shrek":
            shrek()
        elif ayoo == "sausage":
            sausage()


elif app == "instagram":
    bruhh = input("who/what do you want to spam: ")
    ayoo = input("Choose your weapon (bee/shrek/sausage): ")

    if bruhh == "enterprompt":                                #Enter the pre-set prompt that you want to type a particular person on instagram
        promptlink = "enteryourlink"                          #Enter the link of the person's dm 
        os.startfile(promptlink)                              #You can add more prompts of your own to type in your friends' dms
        if ayoo == "bee":
            bee()
        elif ayoo == "shrek":
            shrek()
        elif ayoo == "sausage":
            sausage()