import numpy as np
import kbhit as kb
import pyaudio, wave


# 1 numPy/playNumPy.py simple reproductor con arrays de numPy
import numpy as np # arrays
import pyaudio, kbhit
from scipy.io import wavfile # para manejo de wavs

import pyaudio
import numpy as np

p = pyaudio.PyAudio()

vol = 0.5     # range [0.0, 1.0]
SRATE = 44100       # sampling rate, Hz, must be integer
duration = 10.0   # in seconds, may be float
frec = 440.0        # sine frequency, Hz, may be float
CHUNK = 1024

# generate samples, note conversion to float32 array
data = (np.sin(2 * np.pi * np.arange(SRATE * duration) * frec / SRATE)).astype(np.float32)

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=SRATE,
                output=True)


# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
bloque = np.arange(CHUNK,dtype=data.dtype)
numBloque = 0
kb = kbhit.KBHit()
c= ' '
while c!= 'q':
    # nuevo bloque
    bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]
    bloque *= vol
    # pasamos al stream haciendo conversion de tipo
    stream.write(bloque.astype((data.dtype)).tobytes())
    if kb.kbhit():
        c = kb.getch()
        if (c=='F'):
            vol= max(0,vol-0.05)
        elif (c=='V'):
            vol= min(1,vol+0.05)
        print("Vol: ",vol)
    numBloque += 1


kb.set_normal_term()
stream.stop_stream()
stream.close()
p.terminate()

# play. May repeat with different volume values (if done interactively)


