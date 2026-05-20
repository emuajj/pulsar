import numpy as np
import sounddevice as sd
from pulsar import pulsar_phase,make_main_envelope,make_noise_for_surrounding_enviroment,make_modulations_based_on_axis_rotation,make_sound_synthesis_for_pulses,make_sound_spectral_for_pulses



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
        
    def generate_pulsar(self, t):
        
        f0 = self.state.f0
        f1 = self.state.f1
        f2 = self.state.f2
        
        # CREATING THE PULSES
        phase = pulsar_phase(t, f0, f1, f2)
        
        #TODO CREAR VARIEDAD EN LOS PULSOS SIMULANDO EL DESFASE ENTRE EJE MAGNETICO Y EJE DEL PULSAR . ASÍ COMO INTERFERENCIAS Y RUIDO
        
        beam = make_modulations_based_on_axis_rotation(self.state.magnetic_axis)
        beam = np.clip(beam, 0.0, 1.0)
        
        env = make_main_envelope(phase, self.sr, self.state.view_intensity, beam)
        env = np.clip(env, 0.0, 1.0)
        
        # BUILDING THE SOUND

        # añadimos sintesis para aconseguir musicalmente unos pulsos con frequencias
        mode = self.state.synthesis_mode
        if(mode == 0):
            signal_core = make_sound_synthesis_for_pulses(phase,t,beam,env)
        else:
            signal_core = make_sound_spectral_for_pulses(phase,t,beam,env)

        # AÑADIMOS RUIDO DE FONDO DEL POLVO ESTELAR Y MODULACIONES DEL PULSAR
        noise_dust = make_noise_for_surrounding_enviroment(t)

        # el ruido SOLO reacciona al pulso, no al eje
        pulse_activity = env ** 2

        # modulación física: el pulso “excita” el medio
        noise_dust *= (0.6 + 0.4 * pulse_activity)

        # reverb natural del medio
        decay = 0.7 + 0.3 * (1.0 - self.state.noise_level)

        reverb = np.zeros_like(noise_dust)
        delay = 180

        for i in range(delay, len(noise_dust)):
            reverb[i] = noise_dust[i] + decay * reverb[i - delay]

        space_noise = noise_dust + 0.5 * reverb

        # el ruido crece cuando NO hay pulso (vacío energético)
        space_noise *= (1.0 + 0.5 * (1.0 - env))
        
        # añadir cambio e parametro en GUI
        noise_gain = 1.4 * self.state.noise_level
        space_noise *= noise_gain

        # harmonic fog
        fog = (
            np.sin(2*np.pi*phase*0.5) +
            0.5*np.sin(2*np.pi*phase*1.5) +
            0.25*np.sin(2*np.pi*phase*3.7)
        )
        fog *= (1.0 - env)
        fog *= 0.009
        
        #integrar ruido
        signal = signal_core + space_noise + fog
        
        signal = np.tanh(signal)
        
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