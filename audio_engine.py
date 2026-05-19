import numpy as np
import sounddevice as sd
from pulsar import pulsar_phase,make_main_envelope,make_noise_for_surrounding_enviroment,make_modulations_based_on_axis_rotation



class AudioEngine:
    def __init__(self, state, sr=44100, block=1024):
        self.state = state
        self.sr = sr
        self.block = block
        self.t0 = 0

    def callback(self, outdata, frames, time, status):
        t = (np.arange(frames) + self.t0) / self.sr
        
        res = self.generate_pulsar(t)
        
        self.t0 += frames
        outdata[:] = res.reshape(-1, 1)
        
    def generate_pulsar(self,t):
        
        f0 = self.state.f0
        f1 = self.state.f1
        f2 = self.state.f2
        
        # CREATING THE PULSES
        phase = pulsar_phase(t, f0, f1, f2)
        
        #TODO CREAR VARIEDAD EN LOS PULSOS SIMULANDO EL DESFASE ENTRE EJE MAGNETICO Y EJE DEL PULSAR . ASÍ COMO INTERFERENCIAS Y RUIDO
        
        beam = make_modulations_based_on_axis_rotation(self.state.magnetic_axis)
        
        env = make_main_envelope(phase, self.sr,self.state.view_intensity,beam)
        
        env = np.clip(env, -1.0, 1.0)
        
        # BUILDING THE SOUND

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

        carrier = freqs * (0.6 + 0.4 * beam) + 0.1 * excitation

        # core pulsar
        signal_core = env * carrier
        

        # AÑADIMOS RUIDO DE FONDO DEL POLVO ESTELAR Y MODULACIONES DEL PULSAR
        noise_dust = make_noise_for_surrounding_enviroment(t)

        # modificar ruido cuando el haz no esta alineado
        noise_dust *= (1.0 - beam)

        # modulación suave (no destructiva)
        noise_dust *= (0.6 + 0.4 * env)

        # gain global
        noise_dust *= self.state.noise_level * 3.0

        signal = signal_core + noise_dust
        
        signal = env * carrier
        
        #Ajustar tambien volumen de la senyal en base al punto de vista 
        signal *= 0.2 if self.state.view_intensity <= 0 else self.state.view_intensity
        
        return signal

    def run(self):
        with sd.OutputStream(
            channels=1,
            samplerate=self.sr,
            blocksize=self.block,
            callback=self.callback
        ):
            print("Running real-time synth...") 
            while True:
                sd.sleep(1000)