import numpy as np
from enum import Enum
from scipy import signal
import math
import copy
import matplotlib.pyplot as plt
from note_name import NoteName, note_name_to_freq
from util import SampleRate
from oscillator_params import (WaveformOscillatorParams,
                               WaveformParams,
                               VolumeEnvParams,
                               PitchEnvParams,
                               LowpassParams,
                               HighpassParams,
                               NoiseParams,
                               NoiseWaveformParams,)

class Oscillator:
    def __init__(self,
                 sample_rate: SampleRate):
        self.sample_rate = sample_rate
        self.buff_bare = None
        self.buff = None

    def lowpass_signal(self,
                       lowpass_params: LowpassParams) -> None:
        if lowpass_params.mix == 0:
            return
        if lowpass_params.cutoff < 1:
            cutoff = 1
        elif lowpass_params.cutoff > 20000:
            cutoff = 20000
        else:
            cutoff = lowpass_params.cutoff
        nyquist = self.sample_rate.value / 2
        cutoff_norm = cutoff / nyquist
        # define butter
        b, a = signal.butter(lowpass_params.order.value, cutoff_norm, btype='lowpass')
        # apply filter
        lowpass_buff = copy.deepcopy(self.buff)
        lowpass_buff = signal.filtfilt(b, a, lowpass_buff)
        self.buff = self.mix_buffs(buff1=lowpass_buff,
                              buff2=self.buff,
                              buff1_weight=lowpass_params.mix)

    def highpass_signal(self,
                        highpass_params: HighpassParams) -> None:
        if highpass_params.mix == 0:
            return
        if highpass_params.cutoff < 1:
            cutoff = 1
        elif highpass_params.cutoff > 20000:
            cutoff = 20000
        else:
            cutoff = highpass_params.cutoff
        nyquist = self.sample_rate.value / 2
        cutoff_norm = cutoff / nyquist
        # define butter
        b, a = signal.butter(highpass_params.order.value, cutoff_norm, btype='highpass')
        # apply filter
        highpass_buff = copy.deepcopy(self.buff)
        highpass_buff = signal.filtfilt(b, a, highpass_buff)
        self.buff = self.mix_buffs(buff1=highpass_buff,
                              buff2=self.buff,
                              buff1_weight=highpass_params.mix)
    
    def apply_filter(self,
                     lowpass_params: LowpassParams,
                     highpass_params: HighpassParams) -> None:
        """
        Applies the frequency filter after the signal has been generated.
        """
        self.lowpass_signal(lowpass_params=lowpass_params)
        self.highpass_signal(highpass_params=highpass_params)

    def attack_signal(self,
                      attack_s: float,
                      sharpness: float) -> None:
        """
        - attack: int = num samples (length) of the attack
        - sharpness: float = sharpness of the attack
        """
        attack = int(attack_s * self.sample_rate.value)
        # adjust attack
        for channel in range(len(self.buff)):
            for i in range(attack):
                self.buff[channel][i] *= (i/attack)**sharpness
    
    def decay_signal(self,
                       decay_s: int,
                       sharpness: float) -> None:
        """
        - decay: int = num samples (length) of the decay
        - sharpness: float = sharpness of the decay
        """
        decay = int(decay_s * self.sample_rate.value)
        # adjust release
        for channel in range(len(self.buff)):
            channel_len = len(self.buff[channel])
            # iterate buff in reverse order
            for i in range(decay):
                self.buff[channel][channel_len-i-1] *= (i/decay)**sharpness

    def apply_volume_env(self,
                         volume_env_params: VolumeEnvParams):
        """
        Applies the volume env after the signal has been generated.
        """
        # attack
        self.attack_signal(attack_s=volume_env_params.attack_s,
                           sharpness=volume_env_params.attack_sharpness)
        # decay
        self.decay_signal(decay_s=volume_env_params.decay_s,
                          sharpness=volume_env_params.decay_sharpness)

    def apply_volume_and_filter(self,
                                volume_env_params: VolumeEnvParams,
                                lowpass_params: LowpassParams,
                                highpass_params: HighpassParams) -> None:
        """
        Applies the volume env and filter to the bare signal.
        """
        # first, copy bare buff into buff
        self.buff = copy.deepcopy(self.buff_bare)
        self.apply_volume_env(volume_env_params=volume_env_params)
        self.apply_filter(lowpass_params=lowpass_params,
                          highpass_params=highpass_params)

    def mix_buffs(self,
                  buff1: np.ndarray,
                  buff2: np.ndarray,
                  buff1_weight: float) -> np.ndarray:
        """
        Mixes buff1 and buff2 according to buff1_weight.

        - buff1: np.ndarray = Stereo buffer 1
        - buff2: np.ndarray = Stereo buffer 2
        - buff1_weight: float = weight of buffer 1 (must be between 0.0 and 1.0)\n

        returns -> np.ndarray = Mixed stereo buffer
        """
        if buff1_weight == 1:
            return buff1
        elif buff1_weight == 0:
            return buff2
        if buff1_weight < 0 or buff1_weight > 1:
            print('Error: buff1_weight must be >= 0 and <= 1')
            return
        buff2_weight = 1 - buff1_weight
        buff1 = np.array(buff1) * buff1_weight
        buff2 = np.array(buff2) * buff2_weight
        return np.add(buff1, buff2)
    
    def crossfade_mono_buffs(self,
                             buff1: np.ndarray,
                             buff2: np.ndarray,
                             crossfade_len_s: float) -> np.ndarray:
        """
        Returns a crossfaded buff of the two provided mono buffs.

        - buff1: np.ndarray: mono buff
        - buff2: np.ndarray: mono buff

        returns -> np.ndarray: mono crossfaded buff
        """
        # fade_samples = int(fade_duration * sample_rate)  # Number of samples for the fade
        # fade = np.linspace(0, 1, fade_samples)
        # crossfade = np.concatenate((fade, np.ones(total_samples - 2 * fade_samples), fade[::-1]))

        # # Apply crossfade to the glide waveform
        # glide_waveform[-fade_samples:] *= crossfade[:fade_samples]

        # # Apply crossfade to the constant waveform
        # constant_waveform[:fade_samples] *= crossfade[fade_samples:]

        # # Concatenate the waveforms
        # waveform = np.concatenate((glide_waveform, constant_waveform))

        total_samples = len(buff1) + len(buff2)
        n_fade_samples = int(crossfade_len_s * self.sample_rate.value)
        n_fade_samples = min(n_fade_samples, len(buff1), len(buff2))

        # fade buff1
        fade_for_buff1 = np.linspace(start=1,
                                     stop=0,
                                     num=n_fade_samples)
        buff1_fade = np.multiply(buff1[len(buff1)-n_fade_samples:], fade_for_buff1)

        # fade buff2
        fade_for_buff2 = np.linspace(start=0,
                                     stop=1,
                                     num=n_fade_samples)
        buff2_fade = np.multiply(buff2[:n_fade_samples], fade_for_buff2)

        # merge fades
        merged_fades = np.add(buff1_fade, buff2_fade)

        # merge buffs and fade
        wave = np.concatenate((buff1[:len(buff1)-n_fade_samples], merged_fades, buff2[n_fade_samples:]))

        return wave

class WaveformOscillator(Oscillator):
    """
    Basic waveform oscillator.

    - sample_rate: SampleRate = Sample rate of the oscillator
    """
    def __init__(self,
                 sample_rate: SampleRate):
        super().__init__(sample_rate=sample_rate)

    def __call__(self,
                 waveform_oscillator_params: WaveformOscillatorParams) -> np.ndarray:
        """
        Generates the overall signal for this oscillator. If no waveform and pitch params are provided,
        only applies the volume and filter.

        - waveform_oscillator_params: WaveformOscillatorParams

        returns -> buffer: np.ndarray
        """

        # generate the signal
        if waveform_oscillator_params.waveform_params != None and waveform_oscillator_params.pitch_env_params != None:
            self.generate_buff_bare(waveform_oscillator_params.waveform_params,
                                    waveform_oscillator_params.pitch_env_params)
        # apply volume and filter
        self.apply_volume_and_filter(volume_env_params=waveform_oscillator_params.volume_env_params,
                                     lowpass_params=waveform_oscillator_params.lowpass_params,
                                     highpass_params=waveform_oscillator_params.highpass_params)

        # return buffer
        return self.buff

    def generate_buff_bare(self,
                           waveform_params: WaveformParams,
                           pitch_env_params: PitchEnvParams) -> None:
        """
        Used internally to generate the bare buff. Use the __call__ method instead.
        """
        
        # define frequencies
        final_note = NoteName(waveform_params.fundamental.value + pitch_env_params.range)
        f0 = note_name_to_freq(waveform_params.fundamental)
        f1 = note_name_to_freq(final_note)
        
        # generate the time axis
        n_pitch = int(self.sample_rate.value * pitch_env_params.attack_s)
        t = np.linspace(start=0,
                        stop=waveform_params.len_s,
                        num=int(self.sample_rate.value * waveform_params.len_s),
                        endpoint=False)
        dt = t[1] - t[0]

        # define the frequency sweep
        # sweep = np.logspace(np.log10(f0), np.log10(f1), n)

        _t = np.linspace(0, 1, n_pitch)  # time values from 0 to 1
        # adjust the time values to control sharpness
        t_adjusted = np.power(_t, pitch_env_params.attack_sharpness)
        # compute the frequency sweep
        sweep = f0 + (f1 - f0) * t_adjusted

        # plt.plot(sweep)
        # plt.show()

        # define phase
        phi = 2 * np.pi * np.cumsum(sweep) * dt + waveform_params.phase
        
        # generate the pitch env sine wave
        wave_pitch = waveform_params.mix * np.sin(phi)

        # generate the constant pitch sine wave
        t_const = np.linspace(start=0,
                              stop=waveform_params.len_s - pitch_env_params.attack_s,
                              num=int(self.sample_rate.value * (waveform_params.len_s - pitch_env_params.attack_s)),
                              endpoint=False)
        wave_const = waveform_params.mix * np.sin(2 * np.pi * f1 * t_const)

        # combine the waves
        # wave = np.concatenate((wave_pitch, wave_const))
        CROSSFADE_LEN_S = 0.05
        if CROSSFADE_LEN_S*2 > pitch_env_params.attack_s:
            crossfade_len_s = pitch_env_params.attack_s/2
        else: 
            crossfade_len_s = CROSSFADE_LEN_S
        wave = self.crossfade_mono_buffs(buff1=wave_pitch,
                                         buff2=wave_const,
                                         crossfade_len_s=crossfade_len_s)

        # duplicate for stereo signal
        self.buff_bare = [wave, wave]

class NoiseOscillator(Oscillator):
    """
    Basic noise oscillator.

    - sample_rate: SampleRate =  Sample rate of the oscillator
    """
    def __init__(self,
                 sample_rate: SampleRate):
        super().__init__(sample_rate=sample_rate)

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
