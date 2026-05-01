import numpy as np

import matplotlib.pyplot as plt

class Wave:
    def __init__(self,samples=44100):
        self.samples = samples

    def white(self):
        wave = np.random.normal(0, 1, self.samples)
        wave = np.clip(wave, -3, 3) # 99.7% of values fall within ±3σ naturally
        wave /= 3
        return wave.astype(np.float32)

    def brown(self):
        pass

    def pink(self):
        pass


w = Wave().white()

plt.plot(w)

plt.show()