#coding=utf-8
import matplotlib.pyplot as plt
import wave
import numpy as np
import time

class analyse():
    def __init__(self,audio):
        self.filename = audio
        self.wavefile = wave.open(audio, 'rb')

        params = self.wavefile.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        str_data = self.wavefile.readframes(nframes)
        self.wavefile.close()
        wave_data = np.fromstring(str_data, dtype=np.short)
        wave_data.shape = -1, 2
        self.wave_data = wave_data.T

    def getImg(self):
        plt.subplot(211)
        plt.plot(self.wave_data[0])
        plt.subplot(212)
        plt.plot(self.wave_data[1], c="g")
        img = 'waveforms/{}.jpg'.format(int(time.time()))
        plt.savefig('/srv/flask/qiuqiuqiu/app/'+img)
        plt.close()
        return img