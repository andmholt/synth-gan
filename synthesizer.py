import numpy as np
from note_name import NoteName
from oscillator import WaveformOscillator, NoiseOscillator

class Synthesizer:
    def __init__(self,):
        self.fundamental_osc = WaveformOscillator()
        self.floof_osc = WaveformOscillator()
        # self.noise_osc = NoiseOscillator()
        # self.attack_osc = NoiseOscillator()
    
    def __call__(self, fundamental: NoteName) -> np.ndarray:

        # generate the signals
        fundamental_signal = self.fundamental_osc()
        floof_signal = self.floof_osc()
        # noise_signal = self.noise_osc()
        # attack_signal = self.attack_osc()

        # combine signals
        