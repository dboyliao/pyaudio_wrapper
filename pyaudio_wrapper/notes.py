__all__ = ["C", "D_m", "D",
           "E", "E_m", "F",
           "G_m", "G", "A_m",
           "A", "B_m", "B", "empty",
           "half_empty", "happy", "bee_song"]

import numpy as np
from .audio_data import WavAudioData

SAMPLE_RATE = 16000

x = np.linspace(0, 1, SAMPLE_RATE)

y = (2**8*np.sin(2**(-9./12)*440*2*np.pi*x)).astype(np.int16)
C = 20*WavAudioData(y.tostring(), SAMPLE_RATE, 2, 1, np.int16)[:500]

y = (2**8*np.sin(2**(-8./12)*440*2*np.pi*x)).astype(np.int16)
D_m = 20*WavAudioData(y.tostring(), SAMPLE_RATE, 2, 1, np.int16)[:500]

y = (2**8*np.sin(2**(-7./12)*440*2*np.pi*x)).astype(np.int16)
D = 20*WavAudioData(y.tostring(), SAMPLE_RATE, 2, 1, np.int16)[:500]

y = (2**8*np.sin(2**(-6./12)*440*2*np.pi*x)).astype(np.int16)
E_m = 20*WavAudioData(y.tostring(), SAMPLE_RATE, 2, 1, np.int16)[:500]

y = (2**8*np.sin(2**(-5./12)*440*2*np.pi*x)).astype(np.int16)
E = 20*WavAudioData(y.tostring(), SAMPLE_RATE, 2, 1, np.int16)[:500]

y = (2**8*np.sin(2**(-4./12)*440*2*np.pi*x)).astype(np.int16)
F = 20*WavAudioData(y.tostring(), SAMPLE_RATE, 2, 1, np.int16)[:500]

y = (2**8*np.sin(2**(-3./12)*440*2*np.pi*x)).astype(np.int16)
G_m = 20*WavAudioData(y.tostring(), SAMPLE_RATE, 2, 1, np.int16)[:500]

y = (2**8*np.sin(2**(-2./12)*440*2*np.pi*x)).astype(np.int16)
G = 20*WavAudioData(y.tostring(), SAMPLE_RATE, 2, 1, np.int16)[:500]

y = (2**8*np.sin(2**(-1./12)*440*2*np.pi*x)).astype(np.int16)
A_m = WavAudioData(y.tostring(), SAMPLE_RATE, 2, 1, np.int16)[:500]

y = (2**8*np.sin(440*2*np.pi*x)).astype(np.int16)
A = WavAudioData(y.tostring(), SAMPLE_RATE, 2, 1, np.int16)[:500]

y = (2**8*np.sin(2**(1./12)*440*2*np.pi*x)).astype(np.int16)
B_m = WavAudioData(y.tostring(), SAMPLE_RATE, 2, 1, np.int16)[:500]

y = (2**8*np.sin(2**(2./12)*440*2*np.pi*x)).astype(np.int16)
B = WavAudioData(y.tostring(), SAMPLE_RATE, 2, 1, np.int16)[:500]

empty =  WavAudioData(np.zeros(SAMPLE_RATE, dtype = np.int16).tostring(), SAMPLE_RATE, 2, 1, np.int16)
half_empty = empty[:250]

bee_song = (G + E + E + half_empty + \
    F + D + D + half_empty + \
    C + D + E + F + G + G + G + empty \
    + G + E + E + half_empty + \
    F + D + D + half_empty + \
    C + E + G + G + C + empty + \
    D + D + D + D + D + E + F + half_empty + \
    E + E + E + E + E + F + G + half_empty + \
    G + E + E + half_empty + \
    F + D + D + half_empty + \
    C + E + G + G + C)

happy = E + E + F + G + G + F + E + D + C + C + D + E + E + E[:250] + D[:250] + D[:250]