import numpy as np
import soundfile as sf

def write_wav(buff: np.ndarray, sr: int, path: str, bit_depth: int) -> None:
    # parse bit depth
    subtype = ''
    if bit_depth == 16:
        subtype = 'PCM_16'
    elif bit_depth == 24:
        subtype = 'PCM_24'
    elif bit_depth == 32:
        subtype = 'PCM_32'
    else:
        # unsupported bit depth
        print('ERR in write_wav(): unsupported bit depth of %d' % (bit_depth))
        return
    # check path
    if not path.endswith('.wav'):
        print('ERR in write_wav(): path \'%s\' does not end with \'.wav\'' % (path))
    # write wav
    interleaved_buff = np.vstack((buff[0], buff[1])).T
    sf.write(path, interleaved_buff, sr, subtype)
