import librosa
import librosa.core.audio

def load_audio(path, sr=None, mono=True, offset=0.0, duration=None,
               res_type='kaiser_best'):
    '''
    Load an audio file as a floating point time series.

    :param path: path to the input file. Any format supported by audioread will work.
    :param sr: number > 0 [scalar] target sampling rate ‘None’ uses the native sampling rate
    :param mono: bool convert signal to mono
    :param offset: float - start reading after this time (in seconds)
    :param duration: float - only load up to this much audio (in seconds)
    :param res_type:
    :return: np.ndarray [shape=(n,) or (2, n)] audio time series, sr:number > 0 [scalar] sampling rate of y
    '''

    return librosa.load(path, sr=sr, mono=mono, offset=offset, duration=duration,res_type=res_type)


def mfcc(sig, sr=None, S=None):
    '''
    Parameters
    ----------
    sig : input signal as np.ndarray

    sr : Sample Rate

    n_mfcc: number of MFCCs to return - 20 as default

    dct_type: By default, DCT type-2 is used

    norm: 'norm' or None
        setting norm=’ortho’ uses an ortho-normal DCT basis

    n_fft : int > 0 [scalar]
        length of the FFT window

    hop_length : 'time shift' - through Hanning window

    power : float > 0 [scalar]
        Exponent for the magnitude melspectrogram.
        e.g., 1 for energy, 2 for power, etc.

    '''

    # for sr = 24000 Hz
    kwargs = {
        'n_mfcc': 20,
        'dct_type':2,
        'norm':'ortho',
        'n_fft':int(2048/4),
        'hop_length':int(512/4),
        'power':2.0
    }



    return librosa.feature.mfcc(sig, sr, S, **kwargs)

