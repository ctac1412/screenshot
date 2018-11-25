import pyautogui
import random
import error_log


def move_mouse(x, y):
    try:
        pyautogui.moveTo(x, y, duration=round(random.uniform(0.3, 0.6), 2))
    except Exception as e:
        error_log.error_log('moveMouse', str(e))


def left_click():
    pyautogui.click()
