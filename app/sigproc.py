import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import scipy.special
import time

class SigProc():
    def __init__(self,filename):
        self.filename = filename
        self.signal, self.sr = librosa.load(filename)

    def logMMSE(self):
        x = self.signal
        Slen = int(np.floor(0.02 * self.sr)) - 1
        noise_frames = 6

        PERC = 50
        len1 = int(np.floor(Slen * PERC / 100))
        len2 = Slen - len1

        win = np.hanning(Slen)
        win = win * len2 / np.sum(win)
        nFFT = 2 * Slen

        x_old = np.zeros(len1)
        Xk_prev = np.zeros(len1)
        Nframes = int(np.floor(len(x) / len2) - np.floor(Slen / len2))
        xfinal = np.zeros(Nframes * len2)

        noise_mean = np.zeros(nFFT)
        for j in range(0, Slen * noise_frames, Slen):
            noise_mean = noise_mean + np.absolute(np.fft.fft(win * x[j:j + Slen], nFFT, axis=0))
        noise_mu2 = noise_mean / noise_frames ** 2

        aa = 0.98
        mu = 0.98
        eta = 0.15
        ksi_min = 10 ** (-25 / 10)

        for k in range(0, Nframes * len2, len2):
            insign = win * x[k:k + Slen]

            spec = np.fft.fft(insign, nFFT, axis=0)
            sig = np.absolute(spec)
            sig2 = sig ** 2

            gammak = np.minimum(sig2 / noise_mu2, 40)

            if Xk_prev.all() == 0:
                ksi = aa + (1 - aa) * np.maximum(gammak - 1, 0)
            else:
                ksi = aa * Xk_prev / noise_mu2 + (1 - aa) * np.maximum(gammak - 1, 0)
                ksi = np.maximum(ksi_min, ksi)

            log_sigma_k = gammak * ksi / (1 + ksi) - np.log(1 + ksi)
            vad_decision = np.sum(log_sigma_k) / Slen
            if (vad_decision < eta):
                noise_mu2 = mu * noise_mu2 + (1 - mu) * sig2

            A = ksi / (1 + ksi)
            vk = A * gammak
            ei_vk = 0.5 * scipy.special.expn(1, vk)
            hw = A * np.exp(ei_vk)

            sig = sig * hw
            Xk_prev = sig ** 2
            xi_w = np.fft.ifft(hw * spec, nFFT, axis=0)
            xi_w = np.real(xi_w)

            xfinal[k:k + len2] = x_old + xi_w[0:len1]
            x_old = xi_w[len1:Slen]

        if not np.isnan(xfinal[0]):
            return xfinal
        else:
            return x

    def MFCC(self):
        MFCC = librosa.feature.mfcc(y=self.logMMSE(), sr=self.sr, n_mfcc=40)
        return MFCC


    def PlotImg(self):
        plt.style.use('seaborn-darkgrid')
        plt.rcParams['figure.figsize'] = (8, 6)

        plt.subplot(311)
        librosa.display.waveplot(self.signal, sr=self.sr)
        plt.title('Raw Wave')

        plt.subplot(312)
        librosa.display.waveplot(self.logMMSE(), sr=self.sr)
        plt.title('MMSE-LSA')

        plt.subplot(313)
        librosa.display.specshow(self.MFCC(), x_axis='time')
        plt.colorbar()
        plt.title('MFCC')
        plt.tight_layout()
        img = 'waveforms/{}.jpg'.format(int(time.time()))
        plt.savefig('/srv/flask/qiuqiuqiu/app/'+img)
        plt.close()
        return img


