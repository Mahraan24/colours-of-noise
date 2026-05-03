import time
import config as cg
import threading as td
import wave_generator as wave
import sounddevice as sd

class NoisePlayer:

    def __init__(self):
        self._buffer_size = cg.buffer_size
        self._playing = False
        self._stop_event = td.Event()
        self._volume = cg.volume
        self._thread = None
        self._timer = cg.timer
        self._white_weight = cg.white_weight
        self._brown_weight = cg.brown_weight
        self._pink_weight = cg.pink_weight

    def _stream_loop(self):
        elapsed_ref = [0.0]
        w_white = wave.Wave(samples=self._buffer_size)
        w_brown = wave.Wave(samples=self._buffer_size)
        w_pink = wave.Wave(samples=self._buffer_size)

        def callback(outdata, *_):

            white = w_white.white() * self._white_weight
            pink = w_pink.pink() * self._pink_weight
            brown = w_brown.brown() * self._brown_weight

            buffer = (white + pink + brown) * self._volume

            if self._timer is not None:
                remaining = self._timer - elapsed_ref[0]

                if remaining <= cg.fade_duration:
                    fade_scale = max(0.0, remaining / cg.fade_duration)
                    outdata[:] = (buffer * fade_scale).reshape(-1, 1)
                else:
                    outdata[:] = buffer.reshape(-1, 1)
            else:
                outdata[:] = buffer.reshape(-1, 1)

        with sd.OutputStream(
                samplerate=cg.samplerate,
                blocksize=self._buffer_size,
                channels=1,
                callback=callback
                ):

            start_time = time.time()

            while not self._stop_event.is_set():
                elapsed_ref[0] = time.time() - start_time

                if self._timer is not None and elapsed_ref[0] >= self._timer:
                    break

                self._stop_event.wait(timeout=0.1)

        self._playing = False


    def play(self):
        if self._playing:
            return None
        self._playing = True
        self._stop_event.clear()
        self._thread = td.Thread(target=self._stream_loop,daemon=True)
        self._thread.start()
        return None

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        self._playing = False

    def set_volume(self, volume):
        self._volume = volume

    def set_timer(self, seconds):
        self._timer = seconds

    def set_blend(self, white, pink, brown):
        total = white + pink + brown
        if total == 0:
            self._white_weight = 0.0
            self._pink_weight = 1.0
            self._brown_weight = 0.0
        else:
            self._white_weight = white / total
            self._pink_weight = pink / total
            self._brown_weight = brown / total
