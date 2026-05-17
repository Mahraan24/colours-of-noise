import customtkinter as ctk
from config import *
from utils.preset_manager import *
from utils.ux_controls import make_divider, make_section_label, make_slider, make_play_button


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
        ctk.CTkLabel(
            self.root,
            text=title,
            font=FONT_BOLD,
            text_color=TEXT
        ).pack(pady=(16, 4))

        make_divider(self.root)

        # Noise blend sliders
        self._create_noise_section()

        make_divider(self.root)

        preset_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        preset_frame.pack(pady=10)

        # preset dropdown
        presets = load()
        names = list(presets.keys()) or [no_preset_saved]
        self.dropdown = ctk.CTkOptionMenu(
            preset_frame,
            values=names,
            command=self._on_preset_selected,
            width=200,
            fg_color=SURFACE,
            button_color=ACCENT,
            button_hover_color=RED,
            text_color=TEXT
        )
        self.dropdown.pack(side="left", padx=6)

        #buttons
        ctk.CTkButton(
            preset_frame,
            text=preset_saved,
            command=self._save_preset,
            fg_color=SURFACE,
            hover_color=ACCENT,
            text_color=TEXT,
            width=120
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            preset_frame,
            text=preset_delete,
            command=self._delete_preset,
            fg_color=RED,
            hover_color="#A00000",
            text_color="white",
            width=120
        ).pack(side="left", padx=6)

        # Play / Stop
        make_play_button(self.root, self.on_play, self.on_stop).pack(pady=12)


    def _on_preset_selected(self, name):
        if name == no_preset_saved:
            return None

        presets = load()
        if name not in presets:
            return None

        data = presets[name]
        self._sliders[white].set(data[white])
        self._sliders[pink].set(data[pink])
        self._sliders[brown].set(data[brown])
        self._sliders[volume_tx].set(data[volume_tx])
        self._sliders[timer_tx].set(data[timer_tx])
        self.on_blend(data[white], data[pink], data[brown])
        self.on_volume(data[volume_tx])
        self.on_timer(data[timer_tx] * 60 if data[timer_tx] > 0 else None)

        return None

    def _create_noise_section(self):
        make_section_label(self.root, blend)

        for label, initial in [
            (white, white_weight),
            (pink, pink_weight),
            (brown, brown_weight)
        ]:
            frame, slider = make_slider(
                self.root, label, 0, 1, initial,
                on_change=lambda v, l=label: self._on_blend_change(l, v)
            )
            frame.pack(pady=2)
            self._sliders[label] = slider

        make_divider(self.root)
        make_section_label(self.root, volume_tx)
        frame, slider = make_slider(
            self.root, "vol", 0, 1, volume,
            on_change=self.on_volume
        )
        frame.pack(pady=2)
        self._sliders["volume"] = slider

        make_divider(self.root)
        make_section_label(self.root, "timer")
        frame, slider = make_slider(
            self.root, "min", 0, 60, 0,
            on_change=self._on_timer_change,
            unit=" min",
            integer=True
        )
        frame.pack(pady=2)
        self._sliders["timer"] = slider

    def _on_blend_change(self, changed_label, value):
        white = self._sliders["white"].get()
        pink = self._sliders["pink"].get()
        brown = self._sliders["brown"].get()
        self.on_blend(white,pink,brown)

    def _on_timer_change(self, minutes):
        self.on_timer(int(minutes)*60 if minutes > 0 else None)

    def _save_preset(self):
        dialog = ctk.CTkInputDialog(text="Name your preset:", title="Save Preset")
        name = dialog.get_input()

        if not name:
            return

        data = {
            "white": self._sliders["white"].get(),
            "pink": self._sliders["pink"].get(),
            "brown": self._sliders["brown"].get(),
            "volume": self._sliders["volume"].get(),
            "timer": self._sliders["timer"].get()
        }

        success, msg = save(name, data)
        print(msg)  # replace with a proper message later

        if success:
            # update dropdown with new preset
            presets = load()
            self.dropdown.configure(values=list(presets.keys()))

    def _delete_preset(self):
        name = self.dropdown.get()

        if name == no_preset_saved:
            return

        success, msg = delete(name)
        print(msg)

        if success:
            presets = load()
            names = list(presets.keys()) or [no_preset_saved]
            self.dropdown.configure(values=names)
            self.dropdown.set(names[0])


    def mainloop(self):
        self.root.mainloop()