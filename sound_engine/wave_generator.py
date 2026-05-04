import numpy as np

class Wave:

    def __init__(self,samples=44100):
        self.samples = samples

    def _gaussian(self) -> np.ndarray:
        amps = np.random.normal(0, 1, self.samples)
        return amps.astype(np.float32)

    @staticmethod
    def _normalise(wave, target=0.1) -> np.ndarray:
        rms = np.sqrt(np.mean(wave ** 2))
        wave = wave * (target / (rms + np.finfo(np.float32).eps))
        wave = np.clip(wave, -1, 1)
        return wave.astype(np.float32)

    def white(self) -> np.ndarray:
        wave = self._gaussian()
        return self._normalise(wave, target=0.07)

    def pink(self) -> np.ndarray:
        steps = self._gaussian()
        fft = np.fft.rfft(steps)
        fqs = np.arange(1, len(fft) + 1)
        fft /= np.sqrt(fqs)
        wave = np.fft.irfft(fft, n=self.samples)
        return self._normalise(wave, target=0.09)

    def brown(self) -> np.ndarray:
        steps = self._gaussian()
        fft = np.fft.rfft(steps)
        fqs = np.arange(1, len(fft) + 1)
        fft /= fqs
        wave = np.fft.irfft(fft, n=self.samples)
        return self._normalise(wave, target=0.5)
