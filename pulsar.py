import numpy as np
import soundfile as sf
from presets import PAR_TEXT;
from utils import parse_par


def pulsar_phase(t, f0, f1=0.0, f2=0.0):
    return f0*t + 0.5*f1*t*t + (1.0/6.0)*f2*t*t*t

def make_main_envelope(phase, rng, intensity, beam):

    frac = np.mod(phase, 1.0)

    intensity = np.clip(intensity, 0.0, 1.0)
    beam = np.clip(beam, 0.0, 1.0)

    #JITTER
    c1 = 0.047 + (1.0 - beam) * 0.01 * np.sin(phase * 2*np.pi)

    # base widths
    w_min = 0.010
    w_max = 0.080

    coherence = beam

    w_attack = (w_min + (w_max - w_min) * (1.0 - intensity**2)) * (0.4 + 0.6 * coherence)

    release_factor = 1.0 + 8.0 * (1.0 - intensity)**2 * (1.0 - coherence)
    w_release = w_attack * release_factor

    # circular distance
    dist = np.abs(frac - c1)
    dist = np.minimum(dist, 1.0 - dist)

    left = np.exp(-0.5 * (dist / w_attack)**2)
    right = np.exp(-0.5 * (dist / w_release)**2)

    is_right = frac > c1

    env = np.where(is_right, right, left)

    return env

# Representa el ruido formado por el polvo, plasma , particulas ,... que envuelven un PULSAR debido a su alta fuerza centrifuga
def make_noise_for_surrounding_enviroment(t):
    white = np.random.randn(len(t))

    # 1. low-pass --> ismulando el plasma del pulsar
    dust = np.convolve(white, np.ones(120)/120, mode='same')

    # 2. segundo layer más fino --> simulando las interferencias de radio
    hiss = np.convolve(white, np.ones(15)/15, mode='same')

    # mezcla espectral
    noise = 0.7 * dust + 0.3 * hiss

    # normalización
    noise /= np.max(np.abs(noise) + 1e-8)

    return noise * 0.05



# Representar variabilidad del flujo teniendo en cuenta la rotación del eje magnetico frente al eje del pulsar
def make_modulations_based_on_axis_rotation(magnetic_axis):
    mag_axis = magnetic_axis
    spin_axis = np.array([0, 0, 1])

    mag_axis = mag_axis / (np.linalg.norm(mag_axis) + 1e-8)

    cos_theta = np.clip(np.dot(mag_axis, spin_axis), -1.0, 1.0)
    angle = np.arccos(cos_theta)

    beam = np.exp(-(angle / 0.5) ** 2)
    return beam


def make_sound_synthesis_for_pulses(phase,t,beam,env):
    # añadimos sintesis para aconseguir musicalmente unos pulsos con frequencias
        freqs = (
            np.sin(2*np.pi*phase) +
            0.6*np.sin(2*np.pi*2.7*phase) +
            0.4*np.sin(2*np.pi*5.3*phase) +
            0.2*np.sin(2*np.pi*8.1*phase) +
            1*np.sin(2*np.pi*9*phase)
        )

        excitation = np.random.randn(len(t))
        excitation = np.convolve(excitation, np.ones(10)/10, mode='same')

        carrier = freqs * (1.3 * beam) + 0.1 * excitation

        # core pulsar
        signal_core = env * carrier
        
        return signal_core * 1.2

def make_sound_spectral_for_pulses(phase, t, beam, env):

    harmonics = np.zeros_like(phase)

    density = 20

    instability = 1.0 - beam

    for i in range(1, density):

        jitter = 1.0 + np.random.randn() * 0.02 * instability

        drift = 1.0 + 0.01 * instability * np.sin(phase * 2*np.pi*i)

        amp = 1.0 / (i ** (1.1 + instability))

        #añadimos la onda creada  a partir de jitter , con el drift y la amplificación
        harmonics += amp * np.sin(
            2*np.pi*i*jitter*drift*phase
        )

    # plasma excitation --> aplicamos cierta insetabilidad obteniendo valores random dentro de t i haciendo un convolve para crear una nueva onda
    excitation = np.random.randn(len(t))
    excitation = np.convolve(
        excitation,
        np.ones(6)/6,
        mode='same'
    )

    # combinamos las ondas de los harmonicos con la excitación
    spectral = harmonics + 0.08 * excitation

    signal = env * spectral

    return signal
