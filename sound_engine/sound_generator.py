import config as cg
import threading as td
import wave_generator as wave
import sounddevice as sd

class NoisePlayer:

    def __init__(self):
        self._buffer_size = cg.buffer_size
        self._noise_type = cg.noise_type
        self._playing = False
        self._stop_event = td.Event() #initially false, set() -> true, clear() -> false
        self._volume = cg.volume
        self._thread = None
        self._timer = cg.timer

    def play(self):
        if self._playing:
            return None
        self._playing = True
        self._stop_event.clear()
        self._thread = td.Thread(target=self._stream_loop,daemon=True)
        self._thread.start()
        return None

    def _stream_loop(self):
        w = wave.Wave(samples=self._buffer_size)

        def callback(outdata, *_):
            if self._noise_type == "white":
                buffer_play = w.white()
            elif self._noise_type == "pink":
                buffer_play = w.pink()
            elif self._noise_type == "brown":
                buffer_play = w.brown()
            else:
                raise Exception("Not an acceptable noise.")

            buffer = buffer_play * self._volume
            outdata[:] = buffer.reshape(-1,1)

        with sd.OutputStream(
                samplerate=cg.samplerate,
                blocksize=self._buffer_size,
                channels=1,
                callback=callback
                ):
            while not self._stop_event.is_set():
                self._stop_event.wait(timeout=0.1)

        self._playing = False

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        self._playing = False

    def set_volume(self, volume):
        self._volume = volume

    def set_noise_type(self, noise_type):
        self._noise_type = noise_type

    def set_timer(self, seconds):
        self._timer = seconds

