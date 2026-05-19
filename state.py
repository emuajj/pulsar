# state.py
from presets import PAR_TEXT
from utils import parse_par

class SynthState:
    def __init__(self):
        p = parse_par(PAR_TEXT)

        #Constantes del pulsar.
        self.f0 = float(p["F0"])
        self.f1 = float(p["F1"])
        self.f2 = float(p["F2"])
        
        #Rotación del pulsar en base al espectador
        self.view_intensity = 0.0
        
        #Angulo del eje magnético al eje del pulsar
        self.magnetic_tilt = 0.6      # α (rad)
        self.view_angle = 1.0         # i (rad)
        
        #Parámetros del ruido que envuelve el pulsar
        self.noise_level = 0.5