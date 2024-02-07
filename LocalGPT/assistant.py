from os import system
import speech_recognition as sr
from gpt4all import GPT4All
import sys
import whisper
import warnings
import time
import pyautogui
import webbrowser
import os

model = GPT4All("C:/Users/cptli/Documents/dev/Python/LocalGPT/gpt4all-falcon-newbpe-q4_0.gguf", allow_download=False)
assistant_name = "andy"
listening_for_trigger_word = True
should_run = True
source = sr.Microphone()
recognizer = sr.Recognizer()
tiny_model_path = os.path.expanduser('~/.cache/whisper/tiny.pt')
base_model_path = os.path.expanduser('~/.cache/whisper/base.pt')
tiny_model = whisper.load_model(tiny_model_path)
base_model = whisper.load_model(base_model_path)

if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init() 

tasks = []
listeningToTask = False
askingAQuestion = False

def respond(text):
    if sys.platform == 'darwin':
        ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_$:+-/ ")
        clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
        system(f"say '{clean_text}'")
    else:
        engine.say(text)
        engine.runAndWait()

def check_if_assistant_prompted(audio):
    global listening_for_trigger_word
    with open("wake_word_audio.wav", "wb") as f:
        f.write(audio.get_wav_data())
    result = tiny_model.transcribe("wake_word_audio.wav")
    text = result['text']
    print("You said: ", text)
    if assistant_name in text.lower().strip():
        print("Assitant triggered. Waiting for command")
        listening_for_trigger_word = False

def get_action_text(audio):
    global listening_for_trigger_word
    try:
        with open("command.wav", "wb") as f:
            f.write(audio.get_wav_data())
        result = base_model.transcribe("command.wav")
        text = result['text']
        return text
    except Exception as e:
        print("Error here: ", e)
        listening_for_trigger_word = True
        return None

def listen_callback(recognizer, audio):
    global listening_for_trigger_word
    print("Listening for word ", listening_for_trigger_word)
    if listening_for_trigger_word:
        check_if_assistant_prompted(audio)
        print("Checked if you said it")
    else:
        print("Got a command maybe...")
        result = get_action_text(audio)
        print("Result... ", result)
        if not result or len(result.strip()) == 0:
            print("Error getting command.")
            respond("Failed to understand command.")
        else:
            perform_command(result.lower().strip())
        listening_for_trigger_word = True

def listen_for_command():
    with source as s:
        recognizer.adjust_for_ambient_noise(s, duration=2)
    print("Listening for commands...")
    recognizer.listen_in_background(source, listen_callback)

def listen_for_command_test():
    with source as s:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        with open("command.wav", "wb") as f:
            f.write(audio.get_wav_data())
        command = base_model.transcribe("command.wav")
        if command and command['text']:
            print("You said:", command['text'])
            return command['text'].lower()
        return None
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None

def perform_command(command):
    global tasks
    global listeningToTask
    global askingAQuestion
    global should_run
    global listening_for_trigger_word
    if command:
        print("Command: ", command)
        if listeningToTask:
            tasks.append(command)
            listeningToTask = False
            respond("Adding " + command + " to your task list. You have " + str(len(tasks)) + " currently in your list.")
        elif "add a task" in command:
            listeningToTask = True
            respond("Sure, what is the task?")
        elif "list tasks" in command:
            respond("Sure. Your tasks are:")
            for task in tasks:
                respond(task)
        elif "take a screenshot" in command:
            pyautogui.screenshot("screenshot.png")
            respond("I took a screenshot for you.")
        elif "open chrome" in command:
            respond("Opening Chrome.")
            webbrowser.open("http://www.youtube.com/@JakeEh")
        elif "ask a question" in command:
            askingAQuestion = True
            respond("What's your question?")
            return
        elif askingAQuestion:
            askingAQuestion = False
            respond("Thinking...")
            print("User command: ", command)
            output = model.generate(command, max_tokens=200)
            print("Output: ", output)
            respond(output)
        elif "exit" in command:
            should_run = False
        else:
            respond("Sorry, I'm not sure how to handle that command.")
    listening_for_trigger_word = True

def main():
    global listening_for_trigger_word
    while should_run:
        command = listen_for_command_test()
        if listening_for_trigger_word:
            listening_for_trigger_word = False
        else:
            perform_command(command)
        time.sleep(1)
    respond("Goodbye.")

# def prompt_gpt(audio):
#     global listening_for_trigger_word
#     try:
#         with open("prompt.wav", "wb") as f:
#             f.write(audio.get_wav_data())
#         result = base_model.transcribe('prompt.wav')
#         prompt_text = result['text']
#         if len(prompt_text.strip()) == 0:
#             print("Empty prompt. Please speak again.")
#             respond("Empty prompt. Please speak again.")
#             listening_for_trigger_word = True
#         else:
#             print('User: ' + prompt_text)
#             output = model.generate(prompt_text, max_tokens=200)
#             print('GPT4All: ', output)
#             respond(output)
#             print('\nSay', wake_word, 'to wake me up. \n')
#             listening_for_trigger_word = True
#     except Exception as e:
#         print("Prompt error: ", e)

# def listen_for_wake_word(audio):
#     global listening_for_trigger_word
#     with open("wake_detect.wav", "wb") as f:
#         f.write(audio.get_wav_data())
#     result = tiny_model.transcribe('wake_detect.wav')
#     text_input = result['text']
#     if wake_word in text_input.lower().strip():
#         print("Wake word detected. Please speak your prompt to GPT4All.")
#         respond('Listening')
#         listening_for_trigger_word = False

# def callback(recognizer, audio):
#     global listening_for_trigger_word
#     if listening_for_trigger_word:
#         listen_for_wake_word(audio)
#     else:
#         prompt_gpt(audio)

# def start_listening():
#     with source as s:
#         recognizer.adjust_for_ambient_noise(s, duration=2)
#     print('\nSay', wake_word, 'to wake me up. \n')
#     recognizer.listen_in_background(source, callback)
#     while True:
#         time.sleep(1) 

# if __name__ == '__main__':
#     start_listening() 

if __name__ == "__main__":
#     # print(listen_for_command())
#     respond("This has been building a virtual assistant with Python")
    main()