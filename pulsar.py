import numpy as np
import soundfile as sf
from presets import PAR_TEXT;
from utils import parse_par


def pulsar_phase(t, f0, f1=0.0, f2=0.0):
    return f0*t + 0.5*f1*t*t + (1.0/6.0)*f2*t*t*t

def make_main_envelope(phase, rng,intensity):
    frac = np.mod(phase, 1.0)

    fin_intensity = intensity - 0.4
    if(intensity < 0):
        fin_intensity = 1


    c1 = 0.045 + 0.002
    w1 = 0.020 + 0.003 + fin_intensity
    
    env = (
        1.00 * np.exp(-0.5 * (np.minimum(np.abs(frac - c1), 1 - np.abs(frac - c1)) / w1)**2)
    )    
    
    return env


# Representa el ruido formado por el polvo, plasma , particulas ,... que envuelven un PULSAR debido a su alta fuerza centrifuga
def make_noise_for_surrounding_enviroment(env,t):
    base = np.random.randn(len(t))

    # polvo en formación
    dust = np.convolve(base, np.ones(40)/40, mode='same')

    # modulación por actividad del pulsar
    mod = 0.2 + 0.8 * env

    dust = 0.01 * dust * mod
    
    return dust;