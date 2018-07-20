import pyautogui
import random
import error_log

def moveMouse(x,y):
    try:
        pyautogui.moveTo(x,y,duration=round(random.uniform(0.2, 0.7),2))
    except Exception as e:
        error_log.errorLog('moveMouse',e)

