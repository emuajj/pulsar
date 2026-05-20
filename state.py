# state.py
from presets import PAR_TEXT,PRESETS
from utils import parse_par

class SynthState:
    def __init__(self):
        # p = parse_par(PAR_TEXT)

        # #Constantes del pulsar.
        # self.f0 = float(p["f0"])
        # self.f1 = float(p["f1"])
        # self.f2 = float(p["f2"])

        self.load_preset("crab")
        
        #Rotación del pulsar en base al espectador
        self.view_intensity = 0.0
        
        #Angulo del eje magnético al eje del pulsar
        self.magnetic_tilt = 0.6      # α (rad)
        self.view_angle = 0.6         # i (rad)
        
        #Parámetros del ruido que envuelve el pulsar
        self.noise_level = 0.5
        
        self.world_scale = 1.0

        #Parámetros de witch de modos
        self.synthesis_mode = 0  # 0 = Envelope, 1 = Spectral

        #Preset
        self.current_preset = "crab"

    def load_preset(self, name):
        p = PRESETS[name]
        self.current_preset = name

        # solo inicializa valores base
        self.f0 = float(p["f0"])
        self.f1 = float(p["f1"])
        self.f2 = float(p["f2"])

        self.magnetic_tilt = p["magnetic_tilt"]
        self.noise_level = p["noise_level"]
        self.world_scale = p["world_scale"]