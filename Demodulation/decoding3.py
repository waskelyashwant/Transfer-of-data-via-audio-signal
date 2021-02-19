from scipy.io.wavfile import write
from scipy.io import wavfile
import sounddevice as sd
import numpy as np
import scipy.signal.signaltools as sigtool
import scipy.signal as signal
import time

fc = 2000  # simulate a carrier frequency of 1kHz
fbit = 20  # simulated bitrate of data (Original bitrate was 50 and you have changed it)
fdev = 500  # frequency deviation, make higher than bitrate
Amp = 1  # transmitted signal amplitude
fs = 10000  # sampling frequency for the simulator, must be higher than twice the carrier frequency

def recording():
    seconds = 10  # Duration of recording
    print("start")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write('output.wav', fs, myrecording)
    print("end")


def decodenrz(code):
	prev = 1
	output = ""
	while (len(code)):
		cur = int(code[:1])
		code = code[1:]
		if (cur != prev):
			output += "1"
		else:
			output += "0"
		prev = cur
	return output


def decode(code):
    output = decodenrz(code)
    count=0
    output5=""
    while(count<len(output)):
        output5+='0'
        output5+=output[count:count+7]
        output5+=' '
        count+=8
    ascii_string = ""
    binary_values = output5.split()
    for binary_value in binary_values:
        an_integer = int(binary_value, 2)
        ascii_character = chr(an_integer)
        ascii_string += ascii_character
    return ascii_string


def main_program():
    samplerate, data = wavfile.read('output.wav')
    y = data
    print(y)
    y_diff =np.diff(y,1)
    y_env = np.abs(sigtool.hilbert(y_diff))
    h=signal.firwin(numtaps=100, cutoff=fbit*2, nyq=fs/2)
    y_filtered=signal.lfilter(h, 1.0, y_env)

    mean = np.mean(y_filtered)
    rx_data = ""
    sampled_signal = y_filtered[int(fs / fbit / 2):len(y_filtered):int(fs / fbit)]

    for bit in sampled_signal:
        if bit > mean:
            rx_data += '0'
        else:
            rx_data+='1'

    # rx_data = "11111111111111100000000011111111101010101010101010101010101010101001000111011111001011011101100011010101010101010101011111111110111111111111"
    print(rx_data, type(rx_data))

    k = 0
    j = 0
    len_rx_data = len(rx_data)
    code = ''

    added_string_front1 = "10101010101010101010"

    list1 = []
    flag=0
    for i in range(0, len_rx_data-20):
        a = rx_data[i:i+20]
        if a == added_string_front1:
            k = i+20
            # print(k)
            flag=1
            list1.append(k)
        else:
            if flag==0:
                continue

    for i in range(0, len(list1)):
        if list1[i+1] - list1[i] == 2:
            continue
        else:
            k = list1[i]
            print(k)
            break

    added_string = "10101010101010101010"
    for i in reversed(range(len_rx_data)):
        a = rx_data[i-19:i+1]
        if a == added_string:
            j = i-19
            break

    print(k, j)
    code = rx_data[k:j]
    print(code)

    outpu = decode(code)
    # outpu = decode(rx_data)
    print("message output to bits")
    print(outpu)
    # outpu="yashwant"
    return outpu

# recording()
# main_program()