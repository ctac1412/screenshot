import pyautogui
import random
import error_log


def move_mouse(x, y):
    try:
        pyautogui.moveTo(x, y, duration=round(random.uniform(0.2, 0.5)))
    except Exception as e:
        error_log.error_log('moveMouse', str(e))


def left_click():
    pyautogui.click()
