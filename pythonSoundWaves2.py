import math

import numpy as np
from scipy import signal
import matplotlib.pylab as plt

STRATE = 44100
BUF_SIZE = 1024


def osc(frec,dur):
    x = np.linspace(0, dur, dur*STRATE)
    return x,np.sin(frec * 2 * np.pi * x)


def saw(frec,dur):
    a = 1/frec
    x = np.linspace(0, dur, dur*STRATE)
    #return x, signal.sawtooth(frec * 2 * np.pi * x)
    #return x, np.mod(x*frec,1)
    y= generateSawTooth(x, frec)
    return x, y

def generateSawTooth(x, frec):
    y = []
    for i in x:
        i *= frec
        if int(i)%2 == 1:
            y.append(-i+math.floor(i)+1)
        else:
            y.append(-i+math.floor(i))
    return y


def square(frec,dur):
    x = np.linspace(0, dur, dur*STRATE)
    return x, np.power(-1,np.floor(2*x*frec))


def triangle(frec,dur):
    x = np.linspace(0, dur, dur*STRATE)
    y = generateSawTooth(x, frec)
    y = np.absolute(y)
    return x, y


def vol(factor,sample):
    return sample*factor


def fadeIn(t,sample_x,sample_y):

    for k,v in enumerate(sample_x):
        if v < t:
            sample_y[k] *= (v/t)
        else:
            break
    return sample_y


def fadeOut(t,sample_x,sample_y):
    for k,v in enumerate(sample_x):
        if v >= t:
            sample_y[k] *= 1.0 - ((v-t)/t)
    return sample_y




x_signal, y_signal  = triangle(5,2)
#y_signal = vol(10,y_signal)
#y_signal = fadeOut(1,x_signal,y_signal)
plt.plot(x_signal, y_signal)
plt.xlabel('time in seconds')
plt.ylabel('value')
plt.show()
print("end")


class Osc:
    frec = 0
    currChunk = np.zeros((1,BUF_SIZE))

    def __init__(self,frec):
        self.frec = frec
        self.currChunk = self.nextChunk()

    def nextChunk(self):
        CHUNK_X, CHUNK_Y = osc(self.frec, STRATE/BUF_SIZE)
        return CHUNK_Y


#test_Osc = Osc(10)
#plt.plot(Osc.currChunk)
#plt.show()
