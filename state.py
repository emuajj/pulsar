# state.py
from presets import PAR_TEXT
from utils import parse_par

class SynthState:
    def __init__(self):
        p = parse_par(PAR_TEXT)

        self.f0 = float(p["F0"])
        self.f1 = float(p["F1"])
        self.f2 = float(p["F2"])
        
        
        self.view_intensity = 0.0