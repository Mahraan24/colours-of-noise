import customtkinter as ctk
from utils.ux_controls import *
import config as cg

class Dashboard:

    def __init__(self, on_play, on_stop, on_volume, on_blend, on_timer):
        self.on_play   = on_play
        self.on_stop   = on_stop
        self.on_volume = on_volume
        self.on_blend  = on_blend
        self.on_timer  = on_timer
        self._sliders = {}
        self._build()

    def _build(self):

        pass

    def _on_blend_change(self, changed_label, value):
        pass

    def _on_timer_change(self, minutes):
        pass

    def _on_mode(self, mode):
        pass

    def mainloop(self):
        pass