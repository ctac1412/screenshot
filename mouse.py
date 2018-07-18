import pyautogui
import random
import time

def moveMouse(x,y):
    pyautogui.moveTo(x,y,duration=round(random.uniform(0.2, 0.7),2))

