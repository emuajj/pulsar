# main.py
from state import SynthState
from gui import GUI
from audio_engine import AudioEngine
import threading

state = SynthState()

gui = GUI(state)
audio = AudioEngine(state)

t = threading.Thread(target=audio.run, daemon=True)
t.start()

gui.run()