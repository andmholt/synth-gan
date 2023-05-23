import numpy as np
from enum import Enum
from scipy import signal
from note_name import NoteName

class WaveformParams:
    """
    len_s: length of the waveform in seconds
    mix:
    phase:
    fundamental:
    complexity:
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
    attack:
    decay: 
    """
    def __init__(self,
                 attack: int,
                 decay: int):
        self.attack = attack
        self.decay = decay

class PitchEnvParams:
    """
    range:
    attack:
    decay:
    """
    def __init__(self,
                 range: int,
                 attack: int,
                 decay: int):
        self.range = range
        self.attack = attack
        self.decay = decay

class FilterOrder(Enum):
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5

class LowpassParams:
    """
    mix: 0 - 100\t
    cutoff: cutoff frequency in Hz
    order: sharpness of the lowpass curve
    """
    def __init__(self,
                 mix: float,
                 cutoff: float,
                 order: FilterOrder):
        self.mix = mix
        self.cutoff = cutoff
        self.order = order

class HighpassParams:
    """
    mix: 0 - 100\t
    cutoff: cutoff frequency in Hz
    order: sharpness of the highpass curve
    """
    def __init__(self,
                 mix: float,
                 cutoff: float,
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

class SampleRate(Enum):
    _44100 = 44100
    _48000 = 48000

class Oscillator:
    def __init__(self,
                 sample_rate: SampleRate):
        self.sample_rate = sample_rate

    def lowpass_signal(self,
                       buff: np.ndarray,
                       lowpass_params: LowpassParams) -> np.ndarray:
        nyquist = self.sample_rate / 2
        cutoff_norm = lowpass_params.cutoff / nyquist
        # define butter
        b, a = signal.butter(lowpass_params.order.value, cutoff_norm, btype='lowpass')
        # apply filter
        buff = signal.filtfilt(b, a, buff)
        return buff

    def highpass_signal(self,
                        buff: np.ndarray,
                        highpass_params: HighpassParams) -> np.ndarray:
        nyquist = self.sample_rate / 2
        cutoff_norm = highpass_params.cutoff / nyquist
        # define butter
        b, a = signal.butter(highpass_params.order.value, cutoff_norm, btype='highpass')
        # apply filter
        buff = signal.filtfilt(b, a, buff)
        return buff

class WaveformOscillator(Oscillator):
    def __init__(self):
        super.__init__()

    def __call__(self, waveform_oscillator_params: WaveformOscillatorParams) -> np.ndarray:
        """
        Generates the signal. Use this as opposed to the generate_signal helper function.

        returns -> buffer: np.ndarray
        """

        # generate the signal
        signal = self.generate_signal(waveform_oscillator_params.waveform_params,
                                      waveform_oscillator_params.volume_env_params,
                                      waveform_oscillator_params.pitch_env_params)
        # add lowpass
        signal = self.lowpass_signal(signal,
                                     waveform_oscillator_params.lowpass_params)
        # add highpass
        signal = self.highpass_signal(signal,
                                      waveform_oscillator_params.highpass_params)
        
        # apply mix
        return signal

    def generate_signal(self,
                        waveform_params: WaveformParams,
                        volume_env_params: VolumeEnvParams,
                        pitch_env_params: PitchEnvParams) -> np.ndarray:
        pass

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

class NoiseOscillator(Oscillator):
    def __init__(self,):
        pass

    def __call__(self, noise_params: NoiseParams) -> np.ndarray:
        """
        Generates the noise. Use this as opposed to the generate_signal helper function.

        returns -> buffer: np.ndarray
        """
        
        # generate signal
        signal = self.generate_signal(noise_params.noise_waveform_params,
                                      noise_params.volume_env_params)
        
        # add lowpass
        signal = self.lowpass_signal(signal,
                                     noise_params.lowpass_params)
        
        # add highpass
        signal = self.highpass_signal(signal,
                                      noise_params.highpass_params)
        
        # apply mix
        return signal

    def generate_signal(self,
                        noise_waveform_params: NoiseWaveformParams,
                        volume_env_params: VolumeEnvParams) -> np.ndarray:
        pass
