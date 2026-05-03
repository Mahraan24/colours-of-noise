import numpy as np

class Wave:

    def __init__(self,samples=44100):
        self.samples = samples

    def _gaussian(self) -> np.ndarray:
        return np.random.normal(0, 1, self.samples)

    @staticmethod
    def _normalise(wave) -> np.ndarray:
        rms = np.sqrt(np.mean(wave ** 2))
        wave /= (rms * 3)
        wave = np.clip(wave, -1, 1)
        return wave.astype(np.float32)

    def white(self) -> np.ndarray:
        wave = self._gaussian()
        wave = np.clip(wave, -3, 3)
        wave /= 3
        return wave.astype(np.float32)

    def pink(self) -> np.ndarray:
        steps = self._gaussian()
        fft = np.fft.rfft(steps)
        fqs = np.arange(1, len(fft) + 1)
        fft /= np.sqrt(fqs)
        wave = np.fft.irfft(fft, n=self.samples)
        return self._normalise(wave)

    def brown(self) -> np.ndarray:
        steps = self._gaussian()
        wave = np.cumsum(steps)
        wave -= np.linspace(wave[0], wave[-1], len(wave))
        return self._normalise(wave)