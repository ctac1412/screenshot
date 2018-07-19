import pyautogui
import random

def moveMouse(x,y):
    pyautogui.moveTo(x,y,duration=round(random.uniform(0.2, 0.7),2))

