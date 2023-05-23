import numpy as np
from note_name import NoteName

class Synth:
    def __init__(self,):
        self.fundamental_osc = None
        self.floof_osc = None
        self.noise_osc = None
        self.attack_osc = None
    
    def __call__(self, fundamental: NoteName) -> np.ndarray:
        pass