import numpy as np
import matplotlib.pyplot as plt


class Wave:

    def __init__(self,samples=44100):
        self.samples = samples

    def _gaussian(self):
        return np.random.normal(0, 1, self.samples)

    @staticmethod
    def _normalise(wave):
        rms = np.sqrt(np.mean(wave ** 2))
        wave /= (rms * 3)
        wave = np.clip(wave, -1, 1)
        return wave.astype(np.float32)

    def white(self):
        wave = self._gaussian()
        wave = np.clip(wave, -3, 3)
        wave /= 3
        return wave.astype(np.float32)

    def pink(self):
        steps = self._gaussian()
        fft = np.fft.rfft(steps) #what combination of sine waves makes up this noise signal
        fqs = np.arange(1, len(fft) + 1)
        fft /= np.sqrt(fqs) #go through each sine wave and turning down the volume of the higher freq one.
        wave = np.fft.irfft(fft, n=self.samples)
        return self._normalise(wave)

    def brown(self):
        steps = self._gaussian()
        wave = np.cumsum(steps)
        wave -= np.linspace(wave[0], wave[-1], len(wave))
        return self._normalise(wave)




#for testing
w = Wave().brown()
brown_wave = Wave().brown()
pink_wave = Wave().pink()

for wave, label in [(brown_wave, 'Brown'), (pink_wave, 'Pink')]:
    fft = np.fft.rfft(wave)
    power = np.abs(fft) ** 2
    freqs = np.fft.rfftfreq(len(wave), d=1/44100)
    plt.loglog(freqs[1:], power[1:], label=label)

plt.xlabel("Frequency (Hz)")
plt.ylabel("Power")
plt.title("Brown vs Pink power spectrum")
plt.legend()
plt.show()

plt.plot(w)

plt.show()



