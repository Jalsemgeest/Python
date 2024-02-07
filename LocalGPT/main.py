from os import system
import speech_recognition as sr
from gpt4all import GPT4All
import sys
import whisper
import warnings
import time
import os

# wake_word = 'jarvis'
model = GPT4All("C:/Users/cptli/Documents/dev/Python/LocalGPT/gpt4all-falcon-newbpe-q4_0.gguf", allow_download=False)
r = sr.Recognizer()
tiny_model_path = os.path.expanduser('~/.cache/whisper/tiny.pt')
base_model_path = os.path.expanduser('~/.cache/whisper/base.pt')
# Had to update the ai-stuff\Lib\site-packages\tiktoken_ext\openai_public.py
tiny_model = whisper.load_model(tiny_model_path)
base_model = whisper.load_model(base_model_path)

prompt = model.generate("Can you write me a simple that takes a screenshot of a website in Python? Please only include the code in your response.", max_tokens=200)
print(prompt)

# Leave this like this if you don't need it to be offline
# tiny_model = whisper.load_model('tiny')
# base_model = whisper.load_model('base')