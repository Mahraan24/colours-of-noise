import customtkinter as ctk
from config import *
from utils.preset_manager import *

class Dashboard:

    def __init__(self, on_play, on_stop, on_volume, on_blend, on_timer):
        self.on_play   = on_play
        self.on_stop   = on_stop
        self.on_volume = on_volume
        self.on_blend  = on_blend
        self.on_timer  = on_timer
        self.is_playing = False
        self._sliders = {}
        self._build()

    def _build(self):
        ctk.set_appearance_mode(appearance_mode)
        self.root = ctk.CTk()
        self.root.title(title)
        self.root.geometry(dimension)
        self.root.configure(fg_color=BG)
        self.root.resizable(False,False)

        #title
        title_label = ctk.CTkLabel(
            self.root,
            text=title,
            font=ctk.CTkFont(FONT_BOLD),
            text_color=TEXT
        )
        title_label.place(relx=0.5, rely=0.05, anchor="center")

        #preset dropdown
        presets = load()
        names = list(presets.keys()) or [no_preset_saved]
        self.preset_dropdown = ctk.CTkOptionMenu(
            self.root,
            values=names,
            command=self._on_preset_selected,
            width=200
        )
        self.preset_dropdown.place(relx=0.5, rely=0.1, anchor="center")

        #buttons


    def _on_preset_selected(self, name):
        if name == no_preset_saved:
            return None

        presets = load()
        if name not in presets:
            return None

        data = presets[name]
        self._sliders["white"].set(data["white"])
        self._sliders["pink"].set(data["pink"])
        self._sliders["brown"].set(data["brown"])
        self._sliders["volume"].set(data["volume"])
        self._sliders["timer"].set(data["timer"])
        self.on_blend(data["white"], data["pink"], data["brown"])
        self.on_volume(data["volume"])
        self.on_timer(data["timer"] * 60 if data["timer"] > 0 else None)

        return None

    def _on_blend_change(self, changed_label, value):
        pass

    def _on_timer_change(self, minutes):
        pass

    def _on_mode(self, mode):
        if mode is None:
            return None
        return None

    def mainloop(self):
        self.root.mainloop()