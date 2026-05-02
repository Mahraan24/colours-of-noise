import numpy as np

import matplotlib.pyplot as plt
import sounddevice


class Wave:
    def __init__(self,samples=44100):
        self.samples = samples

    def _gaussian(self):
        return np.random.normal(0, 1, self.samples)

    def white(self):
        wave = self._gaussian()
        wave = np.clip(wave, -3, 3) # 99.7% of values fall within ±3σ naturally
        wave /= 3
        return wave.astype(np.float32)

    def brown(self):
        steps = self._gaussian()
        wave = np.cumsum(steps) #neighbouring samples are related to each other
        rms = np.sqrt(np.mean(wave ** 2)) #root-mean-square
        wave /= (rms * 3)
        wave = np.clip(wave, -1, 1)
        return wave.astype(np.float32)

    def pink(self):
        pass



#for testing
w = Wave().brown()

plt.plot(w)

plt.show()
print("play")
sounddevice.play(w)
sounddevice.wait()