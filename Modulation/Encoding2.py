import numpy as np
import sounddevice as sd
import time
from scipy.io.wavfile import write


fc = 2000  # simulate a carrier frequency of 1kHz
fbit = 20  # simulated bitrate of data (Original bitrate was 50 and you have changed it)
fdev = 500  # frequency deviation, make higher than bitrate
Amp = 1  # transmitted signal amplitude
fs = 10000  # sampling frequency for the simulator, must be higher than twice the carrier frequency


def codenrz(code):
    output = ""
    prev = 1
    while (len(code)):
        cur = code[:1]
        code = code[1:]
        if (cur == "1"):
            prev = (prev + 1) % 2
        output += str(prev)
    return output


def encoding(msg):

    output=' '.join(format(ord(x) if isinstance(x, str) else x,'07b') for x in msg)#it convert every character of msg into binary ascii number of length 7
    #print(output)
    output = codenrz(output)
    print(output)
    output = "000000000111111111110101010101010101010101010101010" + output + "1010101010101010101011111111111"
    return output

def generplay(code):
    """
    Data in
    """
    b = " ".join(code)#separate code in form of binary into distinct '0 and '1'
    c = np.fromstring(b, dtype=int, sep=' ')#this is used for store in b into numpy/array c inform of array
    data_in = c
    N = len(data_in)
   #implementation of VCO
    t = np.arange(0, float(N) / float(fbit), 1 / float(fs), dtype=np.float)
    m = np.zeros(0).astype(float)
    for bit in data_in:
        if bit == 0:
            m = np.hstack((m, np.multiply(np.ones(int(fs / fbit)), fc + fdev)))
        else:
            m = np.hstack((m, np.multiply(np.ones(int(fs / fbit)), fc - fdev)))
    y = np.zeros(0)
    y = Amp * np.cos(2 * np.pi * np.multiply(m, t))
    waveform_integers = np.int16(y * 32767)
    write("1.wav", fs, waveform_integers)
    return y

def input_string(input_str):
    while True:
        try:
            # input = input()
            input = input_str
        except EOFError:
            break

        if (input == ""):
            break
        else:
            inputspl = input
            output = encoding(inputspl)
            # print("Message input to bits :: ", output)
            print(output)
            y=generplay(output)
            # print(y)
            sd.play(y,fs)
            time.sleep(12)
        print("Generating completed.")
        break

# input_string("communication")