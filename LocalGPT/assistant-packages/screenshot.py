import pyautogui
import datetime

# Generate a filename with a timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"screenshot_{timestamp}.png"

# Take a screenshot using pyautogui
screenshot = pyautogui.screenshot()

# Save the screenshot to the same folder as the script
screenshot.save(filename)

print(f"Screenshot saved as {filename}")
