import numpy as np
import soundfile as sf
import sounddevice as sd
from enum import Enum
import matplotlib.pyplot as plt
import librosa
from typing import Tuple
import time

class FilterOrder(Enum):
    """
    For filters.
    """
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5

class SampleRate(Enum):
    _44100 = 44100
    _48000 = 48000

class BitDepth(Enum):
    _16 = 16
    _24 = 24
    _32 = 32

def plot_wave(buff: np.ndarray) -> None:
    """
    Plots the buffer.

    - buff: np.ndarray = The buffer to plot
    """
    fig = plt.figure()
    fig.suptitle('Waveform')
    # first channel
    left = fig.add_subplot(211)
    left.title.set_text('Left')
    left.plot(buff[0])
    left.set_ylim([-1, 1])
    # second channel
    right = fig.add_subplot(212)
    right.title.set_text('Right')
    right.plot(buff[1])
    right.set_ylim([-1, 1])
    # show
    fig.tight_layout(pad=1.0)
    plt.show()

def write_wav(buff: np.ndarray, sr: SampleRate, path: str, bit_depth: BitDepth) -> None:
    """
    Writes a wav file to the specified path.

    - buff: np.ndarray = Stereo buffer to write as wav
    - sr: SampleRate = Sample rate of the buffer/wav file
    - path: str = Path and name of the wav file (must end with '.wav')
    - bit_depth: BitDepth: Bit depth of the wav file
    """
    # parse bit depth
    bit_depth_str = ''
    if bit_depth.value == 16:
        bit_depth_str = 'PCM_16'
    elif bit_depth.value == 24:
        bit_depth_str = 'PCM_24'
    elif bit_depth.value == 32:
        bit_depth_str = 'PCM_32'
    else:
        # unsupported bit depth
        print('ERR in write_wav(): unsupported bit depth of %d' % (bit_depth.value))
        return
    # check path
    if not path.endswith('.wav'):
        print('ERR in write_wav(): path \'%s\' does not end with \'.wav\'' % (path))
    # write wav
    interleaved_buff = np.vstack((buff[0], buff[1])).T
    sf.write(path, interleaved_buff, sr.value, bit_depth_str)

def play_buff(buff: np.ndarray, sr: SampleRate) -> None:
    """
    Plays the audio buffer.

    buff: np.ndarray = Stereo audio buffer
    sr: SampleRate = Sample rate of the buffer
    """
    # pad to avoid playback clipping
    pad = np.zeros((int(sr.value*0.25)))
    left = np.concatenate((buff[0], pad))
    right = np.concatenate((buff[1], pad))
    sd.play(np.column_stack((left, right)), sr.value)
    sd.wait()

def read_wav(path: str) -> Tuple[np.ndarray, SampleRate]:
    buff, sr = librosa.load(path, sr=None, mono=False)
    return (buff, SampleRate(sr))