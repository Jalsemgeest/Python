#!/usr/bin/env python3

import pyautogui
import time


pyautogui.moveTo(100, 500, duration=1)

time.sleep(2) # 2 seconds

pyautogui.moveTo(500, None, duration=1.5) # uses the same Y as before




















pyautogui.click()

# You can also click at specific coordinates
# pyautogui.click(x, y)




















pyautogui.typewrite("Hello, world!", interval=0.2)
pyautogui.press('enter')
pyautogui.keyDown('shift')
pyautogui.write('uppercase')
pyautogui.keyUp('shift')
































# print(pyautogui.alert(text="text", title="title", button="OK"))

# print(pyautogui.confirm(text='text', title='title', buttons=['OK', 'CANCEL'])) # returns text of button clicked on

# print(pyautogui.prompt(text='text', title='title', default='default')) # returns input text

# print(pyautogui.password(text='text', title='title', default='default', mask='*'))




















# import keyboard

# counter = 0

# def saveScreenshot():
#     global counter
#     filename = "screenshot-" + str(counter) + ".png"
#     pyautogui.screenshot(filename)
#     counter = counter + 1
    
# keyboard.add_hotkey('space', saveScreenshot)
# keyboard.wait()

