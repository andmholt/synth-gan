from util import FilterOrder
from note_name import NoteName

class WaveformParams:
    """
    - len_s: float = Length of the waveform in seconds
    - mix: float = 0.0 - 1.0
    - phase: float =
    - fundamental: NoteName = 
    - complexity: ?
    """
    def __init__(self,
                 len_s: float,
                 mix: float,
                 phase: float,
                 fundamental: NoteName,
                 complexity: int):
        self.len_s = len_s
        self.mix = mix
        self.phase = phase
        self.fundamental = fundamental
        self.complexity = complexity

class VolumeEnvParams:
    """
    - attack: int = num samples (length) of the attack
    - attack_sharpness: int = sharpness of the attack
    - decay: int = num samples (length) of the decay
    - decay_sharpness: int = sharpness of the decay
    """
    def __init__(self,
                 attack_s: float,
                 attack_sharpness: int,
                 decay_s: float,
                 decay_sharpness: int):
        self.attack_s = attack_s
        self.attack_sharpness = attack_sharpness
        self.decay_s = decay_s
        self.decay_sharpness = decay_sharpness

class PitchEnvParams:
    """
    - range: int = range in semitones
    - attack_s: length of the pitch env
    - attack_sharpness: float = (0, 1) for exponential; > 1 for logarithmic
    """
    def __init__(self,
                 range: int,
                 attack_s: int,
                 attack_sharpness: float):
        self.range = range
        self.attack_s = attack_s
        self.attack_sharpness = attack_sharpness

class LowpassParams:
    """
    - mix: float = 0.0 - 1.0
    - cutoff: int = cutoff frequency in Hz
    - order: FilterOrder = sharpness of the lowpass curve
    """
    def __init__(self,
                 mix: float,
                 cutoff: int,
                 order: FilterOrder):
        self.mix = mix
        self.cutoff = cutoff
        self.order = order

class HighpassParams:
    """
    - mix: float = 0.0 - 1.0
    - cutoff: int = cutoff frequency in Hz
    - order: FilterOrder = sharpness of the highpass curve
    """
    def __init__(self,
                 mix: float,
                 cutoff: int,
                 order: FilterOrder):
        self.mix = mix
        self.cutoff = cutoff
        self.order = order
    
class WaveformOscillatorParams:
    """
    - waveform_params
    - volume_env_params
    - pitch_env_params
    - lowpass_params
    - highpass_params
    """
    def __init__(self,
                 waveform_params: WaveformParams,
                 volume_env_params: VolumeEnvParams,
                 pitch_env_params: PitchEnvParams,
                 lowpass_params: LowpassParams,
                 highpass_params: HighpassParams):
        self.waveform_params = waveform_params
        self.volume_env_params = volume_env_params
        self.pitch_env_params = pitch_env_params
        self.lowpass_params = lowpass_params
        self.highpass_params = highpass_params

class NoiseWaveformParams:
    def __init__(self,
                 mix: float):
        self.mix = mix

class NoiseParams:
    """
    - noise_waveform_params
    - volume_env_params
    - lowpass_params
    - highpass_params
    """
    def __init__(self,
                 noise_waveform_params: NoiseWaveformParams,
                 volume_env_params: VolumeEnvParams,
                 lowpass_params: LowpassParams,
                 highpass_params: HighpassParams):
        self.noise_waveform_params = noise_waveform_params
        self.volume_env_params = volume_env_params
        self.lowpass_params = lowpass_params
        self.highpass_params = highpass_params