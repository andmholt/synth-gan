import sys
sys.path.append('..')
from util import read_wav, play_buff, plot_wave
import sounddevice as sd

ref_buff, ref_sr = read_wav('../refs/DBM_CK_KICK_10.wav')
# plot_wave(ref_buff)
play_buff(ref_buff, ref_sr)