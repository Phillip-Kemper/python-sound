import numpy as np
import kbhit as kb
import pyaudio, wave
import math
import matplotlib.pylab as plt

vol = 0.5     # range [0.0, 1.0]
SRATE = 44100       # sampling rate, Hz, must be integer
duration = 10.0   # in seconds, may be float
frec = 440.0        # sine frequency, Hz, may be float
CHUNK = 1024

def osc():
    return (np.sin(2 * np.pi * np.arange(SRATE * duration) * frec / SRATE)).astype(np.float32)
    #x = np.linspace(0, dur, dur*SRATE)
    #return x,np.sin(frec * 2 * np.pi * x)


def saw():
    x = np.linspace(0, duration, int(duration)*SRATE)
    #return x, signal.sawtooth(frec * 2 * np.pi * x)
    #return x, np.mod(x*frec,1)
    y= generateSawTooth(x)
    return y

def generateSawTooth(x):
    y = []
    for i in x:
        i *= frec
        if int(i)%2 == 1:
            y.append(-i+math.floor(i)+1)
        else:
            y.append(-i+math.floor(i))
    return y


def square():
    #x = np.linspace(0, duration, duration*SRATE)
    return np.power(-1,np.floor(2*frec/SRATE*np.arange(SRATE * duration)))


def triangle():
    x = np.linspace(0, duration, int(duration)*SRATE)
    y = generateSawTooth(x)
    y = np.absolute(y)
    return y

p = pyaudio.PyAudio()



# generate samples, note conversion to float32 array
#data = (np.sin(2 * np.pi * np.arange(SRATE * duration) * frec / SRATE)).astype(np.float32)
data = triangle()

plt.plot(data)
plt.xlabel('time in seconds')
plt.ylabel('value')
plt.show()

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=SRATE,
                output=True)


# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
#bloque = np.arange(CHUNK,dtype=data.dtype)
numBloque = 0
kb = kb.KBHit()
c= ' '
while c!= 'q':
    # nuevo bloque

#    data = (np.sin(2 * np.pi * np.arange(SRATE * duration) * frec / SRATE)).astype(np.float32)
    data = square()

    bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]

    bloque *= vol
#    bloque *= frec/SRATE
    # pasamos al stream haciendo conversion de tipo
    stream.write(bloque.astype((data.dtype)).tobytes())
    if kb.kbhit():
        c = kb.getch()
        if (c=='-'):
            vol= max(0,vol-0.05)
        elif (c=='+'):
            vol= min(1,vol+0.05)
        print("Vol: ",vol)

        if (c=='F'):
            frec+= 20
        elif (c=='f'):
            frec -= 20
        print("Frec: ",frec)




    numBloque += 1


kb.set_normal_term()
stream.stop_stream()
stream.close()
p.terminate()

# play. May repeat with different volume values (if done interactively)


