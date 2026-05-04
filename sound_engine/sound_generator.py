import numpy as np
import time
import config as cg
import threading as td
import sounddevice as sd
import sound_engine.wave_generator as wave

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
        long_buffer_seconds = 30

        w_white = wave.Wave(samples=cg.samplerate * long_buffer_seconds)
        w_pink = wave.Wave(samples=cg.samplerate * long_buffer_seconds)
        w_brown = wave.Wave(samples=cg.samplerate * long_buffer_seconds)

        white_loop = w_white.white()
        white_pos = [0]

        pink_loop = w_pink.pink()
        pink_pos = [0]

        brown_loop = w_brown.brown()
        brown_pos = [0]

        def callback(outdata, *_):
            #=====================White=====================
            start_white = white_pos[0]
            end_white = start_white + self._buffer_size

            if end_white <= len(white_loop):
                chunk = white_loop[start_white:end_white]
            else:
                # wrap around — stitch end + beginning
                chunk = np.concatenate([
                    white_loop[start_white:],
                    white_loop[:end_white - len(white_loop)]
                ])

            white_pos[0] = end_white % len(white_loop)
            white = chunk * self._white_weight
            #=====================White=====================

            #=====================Pink=====================
            start_pink = pink_pos[0]
            end_pink = start_pink + self._buffer_size

            if end_pink <= len(pink_loop):
                chunk = pink_loop[start_pink:end_pink]
            else:
                # wrap around — stitch end + beginning
                chunk = np.concatenate([
                    pink_loop[start_pink:],
                    pink_loop[:end_pink - len(pink_loop)]
                ])

            pink_pos[0] = end_pink % len(pink_loop)
            pink = chunk * self._pink_weight
            #=====================Pink=====================

            #=====================Brown=====================
            start_brown = brown_pos[0]
            end_brown = start_brown + self._buffer_size

            if end_brown <= len(brown_loop):
                chunk = brown_loop[start_brown:end_brown]
            else:
                # wrap around — stitch end + beginning
                chunk = np.concatenate([
                    brown_loop[start_brown:],
                    brown_loop[:end_brown - len(brown_loop)]
                ])

            brown_pos[0] = end_brown % len(brown_loop)
            brown = chunk * self._brown_weight
            #=====================Brown=====================

            buffer = (white + pink + brown) * self._volume
            peak = np.max(np.abs(buffer))
            if peak > 1.0:
                buffer /= peak

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
