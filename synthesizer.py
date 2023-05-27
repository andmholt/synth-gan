import numpy as np
import copy
from note_name import NoteName
from oscillator import WaveformOscillator, NoiseOscillator
from oscillator_params import WaveformOscillatorParams, VolumeEnvParams, LowpassParams, HighpassParams
from util import SampleRate

class Synthesizer:
    """
    Synthesizer

    - sample_rate: SampleRate = Sample rate of the synthesizer
    - len_s: float = Initial desired length (seconds) of the synthesized signal
    """
    def __init__(self,
                 sample_rate: SampleRate):
        self.sample_rate = sample_rate

        self.fundamental_osc = WaveformOscillator(sample_rate=sample_rate)
        self.floof_osc = WaveformOscillator(sample_rate=sample_rate)
        # self.noise_osc = NoiseOscillator()
        # self.attack_osc = NoiseOscillator()

        self.main_buff = None
    
    def __call__(self,
                 fundamental_osc_params: WaveformOscillatorParams,
                 floof_osc_params: WaveformOscillatorParams) -> np.ndarray:
        """
        Generate and sum the signals

        - fundamental_osc_params: WaveformOscillatorParams
        - floof_osc_params: WaveformOscillatorParams

        returns -> np.ndarray: The overall generated signal
        """
        # generate the signals
        self.fundamental_osc(waveform_oscillator_params=fundamental_osc_params)
        self.floof_osc(waveform_oscillator_params=floof_osc_params)
        # noise_signal = self.noise_osc()
        # attack_signal = self.attack_osc()

        # combine signals
        self.sum_buffs()

        return self.main_buff
    
    def set_len_s_and_gen(self,
                          len_s: float) -> None:
        """
        Set the length of the synthesizer and re-generate with the new length.

        - len_s: float
        - fundamental_osc_params: WaveformOscillatorParams
        - floof_osc_params: FloofOscillatorParams
        """
        self.len_s = len_s
        # set osc len_s and regenerate

    def resize_buff(self,
                    buff: np.ndarray,
                    new_size: int) -> np.ndarray:
        """
        Used internally to resize buffs.
        """
        return [np.pad(buff[0], (0, new_size - len(buff[0])), mode='constant'),
                np.pad(buff[1], (0, new_size - len(buff[1])), mode='constant')]
    
    def sum_buffs(self) -> None:
        """
        Used internally to sum the oscillators.
        """
        # if either buff is not set yet, set main_buff to the buff that is set
        if self.fundamental_osc.buff == None:
            self.main_buff = copy.deepcopy(self.floof_osc.buff)
            return
        elif self.floof_osc.buff == None:
            self.main_buff = copy.deepcopy(self.fundamental_osc.buff)
            return
        num_oscs = 2
        buff_weight = 1 / num_oscs
        # if buffs are the same size, combine and continue
        if len(self.fundamental_osc.buff[0]) == len(self.floof_osc.buff[0]):
            self.main_buff = np.add(np.array(self.fundamental_osc.buff)*buff_weight,
                                    np.array(self.floof_osc.buff)*buff_weight)
        # else resize
        elif len(self.fundamental_osc.buff[0]) > len(self.floof_osc.buff[0]):
            # fundamental buff is larger
            resized_floof_buff = self.resize_buff(self.floof_osc.buff, len(self.fundamental_osc.buff[0]))
            self.main_buff = np.add(np.array(self.fundamental_osc.buff)*buff_weight,
                                    np.array(resized_floof_buff)*buff_weight)
        elif len(self.fundamental_osc.buff[0]) < len(self.floof_osc.buff[0]):
            # floof buff is larger
            resized_fundamental_buff = self.resize_buff(self.fundamental_osc.buff, len(self.floof_osc.buff[0]))
            self.main_buff = np.add(np.array(self.floof_osc.buff)*buff_weight,
                                    np.array(resized_fundamental_buff)*buff_weight)
        
    def submit_new_fundamental(self,
                               fundamental_params: WaveformOscillatorParams) -> np.ndarray:
        """
        Submit new fundamental params to re-generate only the fundamental signal.

        - fundamental_params: WaveformOscillatorParams

        returns -> np.ndarray = The overall generated signal
        """
        self.fundamental_osc(waveform_oscillator_params=fundamental_params)
        self.sum_buffs()
        return self.main_buff

    def submit_new_fundamental_supps(self,
                                       volume_env_params: VolumeEnvParams,
                                       lowpass_params: LowpassParams,
                                       highpass_params: HighpassParams) -> np.ndarray:
        """
        Submit new fundamental volume and filter params to re-apply to only the fundamental signal.

        - volume_env_params: VolumeEnvParams
        - lowpass_params: LowpassParams
        - highpass_params: HighpassParams

        returns -> np.ndarray = The overall generated signal
        """
        fundamental_params = WaveformOscillatorParams(waveform_params=None,
                                                      volume_env_params=volume_env_params,
                                                      pitch_env_params=None,
                                                      lowpass_params=lowpass_params,
                                                      highpass_params=highpass_params)
        self.fundamental_osc(waveform_oscillator_params=fundamental_params)
        self.sum_buffs()
        return self.main_buff
    
    def submit_new_floof(self,
                         floof_params: WaveformOscillatorParams) -> np.ndarray:
        """
        Submit new floof params to re-generate only the floof signal.

        - floof_params: WaveformOscillatorParams

        returns -> np.ndarray = The overall generated signal
        """
        self.floof_osc(waveform_oscillator_params=floof_params)
        self.sum_buffs()
        return self.main_buff
    
    def submit_new_floof_supps(self,
                               volume_env_params: VolumeEnvParams,
                               lowpass_params: LowpassParams,
                               highpass_params: HighpassParams) -> np.ndarray:
        """
        Submit new floof volume and filter params to re-apply to only the floof signal.

        - volume_env_params: VolumeEnvParams
        - lowpass_params: LowpassParams
        - highpass_params: HighpassParams

        returns -> np.ndarray = The overall generated signal
        """
        floof_params = WaveformOscillatorParams(waveform_params=None,
                                                volume_env_params=volume_env_params,
                                                pitch_env_params=None,
                                                lowpass_params=lowpass_params,
                                                highpass_params=highpass_params)
        self.floof_osc(waveform_oscillator_params=floof_params)
        self.sum_buffs()
        return self.main_buff