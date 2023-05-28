import sys
sys.path.append('..')
from oscillator import WaveformOscillator
from oscillator_params import (WaveformParams,
                               VolumeEnvParams,
                               PitchEnvParams,
                               LowpassParams,
                               HighpassParams,
                               WaveformOscillatorParams)
from note_name import NoteName
from util import write_wav, FilterOrder, SampleRate, BitDepth, plot_wave, play_buff

waveform_params = WaveformParams(len_s=3,
                                 mix=1,
                                 phase=0,
                                 fundamental=NoteName.A_5,
                                 complexity=0)
volume_params = VolumeEnvParams(attack_s=0,
                                attack_sharpness=5,
                                decay_s=0,
                                decay_sharpness=5)
pitch_params = PitchEnvParams(range=-12,
                              attack_s=1.5,
                              attack_sharpness=1)
lowpass_params = LowpassParams(mix=0,
                               cutoff=12000,
                               order=FilterOrder._4)
highpass_params = HighpassParams(mix=0,
                                 cutoff=600,
                                 order=FilterOrder._4)

params = WaveformOscillatorParams(waveform_params=waveform_params,
                                  volume_env_params=volume_params,
                                  pitch_env_params=pitch_params,
                                  lowpass_params=lowpass_params,
                                  highpass_params=highpass_params)

osc = WaveformOscillator(sample_rate=SampleRate._44100)

signal = osc(waveform_oscillator_params=params)
play_buff(signal, SampleRate._44100)
# plot_wave(signal)
# write_wav(signal, SampleRate._44100, 'test.wav', BitDepth._16)
