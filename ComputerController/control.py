import pygame
import pyautogui

pygame.init()

pygame.joystick.init()

joysticks = []

# 1. Get button presses from the controller
# 2. Make button presses click
# 3. Get joystick movements from the controller
# 4. Make joystick move the mouse

###

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.JOYDEVICEADDED:
#             print("Adding device")
#             joy = pygame.joystick.Joystick(event.device_index)
#             joysticks.append(joy)
#     for joystick in joysticks:
#         if joystick.get_button(0):
#             print("subscribe")
        
























# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.JOYDEVICEADDED:
#             print("Adding device")
#             joy = pygame.joystick.Joystick(event.device_index)
#             joysticks.append(joy)
#     for joystick in joysticks:
#         # X
#         if joystick.get_button(0):
#             print("0")
#         # Circle
#         if joystick.get_button(1):
#             print("1")
#         # Square
#         if joystick.get_button(2):
#             print("2")
#         # Triangle
#         if joystick.get_button(3):
#             print("3")
#         # DPad
#         if joystick.get_button(14):
#             print("right")
#         if joystick.get_button(13):
#             print("left")
#         if joystick.get_button(11):
#             print("up")
#         if joystick.get_button(12):
#             print("down")




















# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.JOYDEVICEADDED:
#             print("Adding device")
#             joy = pygame.joystick.Joystick(event.device_index)
#             joysticks.append(joy)
#     for joystick in joysticks:
#         if joystick.get_button(0):
#             pyautogui.click()




























# lastPressedX = 0
# pressLength = 300

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.JOYDEVICEADDED:
#             print("Adding device")
#             joy = pygame.joystick.Joystick(event.device_index)
#             joysticks.append(joy)
#     for joystick in joysticks:
#         time = pygame.time.get_ticks()
#         if joystick.get_button(0):
#             if (time - pressLength) >= lastPressedX:
#                     lastPressedX = time
#                     pyautogui.click()






















# lastPressedX = 0
# lastPressedCircle = 0
# lastPressedTriangle = 0
# pressLength = 300

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.JOYDEVICEADDED:
#             print("Adding device")
#             joy = pygame.joystick.Joystick(event.device_index)
#             joysticks.append(joy)
    
#     # left stick joystick.get_axis(0) - left: -1, right: 1
#     # left stick joystick.get_axis(1) - up: -1, down: 1
#     # right stick joystick.get_axis(2) - left: -1, right: 1
#     # right stick joystick.get_axis(3) - up: -1, down: 1
#     for joystick in joysticks:
#         print(f'left/right: {joystick.get_axis(0)} - up/down: {joystick.get_axis(1)}')


























# lastPressedX = 0
# lastPressedCircle = 0
# lastPressedTriangle = 0
# takeInputs = True
# pressLength = 300

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            print("Adding device")
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joy)
    
    # Joystick and button presses
    for joystick in joysticks:
        # Button Presses
        time = pygame.time.get_ticks()
        # X
        if joystick.get_button(0):
            if (time - pressLength) >= lastPressedX:
                lastPressedX = time
                pyautogui.click()
        # Circle
        if joystick.get_button(1):
            if (time - pressLength) >= lastPressedCircle:
                lastPressedCircle = time
                pyautogui.click(button="secondary")
        # Triangle
        if joystick.get_button(3):
            print("Pressing triangle")
            if (time - pressLength) >= lastPressedTriangle:
                lastPressedTriangle = time

        # Joystick Movement
        changeY = joystick.get_axis(1) * 50
        changeX = joystick.get_axis(0) * 50

        mX, mY = pyautogui.position()
        width, height = pyautogui.size()

        newMX = max(0, min(mX + changeX, width))
        newMY = max(0, min(mY + changeY, height))

        pyautogui.moveTo(newMX, newMY)























# lastPressedX = 0
# lastPressedCircle = 0
# lastPressedTriangle = 0
# takeInputs = True
# pressLength = 300

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.JOYDEVICEADDED:
#             print("Adding device")
#             joy = pygame.joystick.Joystick(event.device_index)
#             joysticks.append(joy)
    
#     # Joystick and button presses
#     for joystick in joysticks:
#         # Button presses
#         time = pygame.time.get_ticks()
#         if takeInputs:
#             # X
#             if joystick.get_button(0):
#                 if (time - pressLength) >= lastPressedX:
#                     lastPressedX = time
#                     pyautogui.click()
#             # Circle
#             if joystick.get_button(1):
#                 if (time - pressLength) >= lastPressedCircle:
#                     lastPressedCircle = time
#                     pyautogui.click(button="secondary")
#         # Triangle
#         if joystick.get_button(3):
#             print("Pressing triangle")
#             if (time - pressLength) >= lastPressedTriangle:
#                 lastPressedTriangle = time
#                 takeInputs = not takeInputs
        
#         # Joystick Movement
#         if takeInputs:
#             changeY = joystick.get_axis(1) * 50
#             changeX = joystick.get_axis(0) * 50

#             mX, mY = pyautogui.position()
#             width, height = pyautogui.size()

#             newMX = max(0, min(mX + changeX, width))
#             newMY = max(0, min(mY + changeY, height))

#             pyautogui.moveTo(newMX, newMY)


































# # X
        # if joystick.get_button(0):
        #     print(pygame.time.get_ticks())
        #     print("0")
        # # Circle
        # if joystick.get_button(1):
        #     print("1")
        # # Square
        # if joystick.get_button(2):
        #     print("2")
        # # Triangle
        # if joystick.get_button(3):
        #     print("3")
        # DPad
        # if joystick.get_button(14):
        #     print("right")
        # if joystick.get_button(13):
        #     print("left")
        # if joystick.get_button(11):
        #     print("up")
        # if joystick.get_button(12):
        #     print("down")
        # print(f'left/right: {joystick.get_axis(0)} - up/down: {joystick.get_axis(1)}')
        # print(joystick.get_axis(2))