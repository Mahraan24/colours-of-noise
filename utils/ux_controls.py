import customtkinter as ctk
import tkinter as tk
from config import *

def make_divider(parent):
    line = tk.Frame(parent, bg=DIVIDER, height=1)
    line.pack(fill="x", padx=20, pady=6)

def make_section_label(parent, text):
    lbl = ctk.CTkLabel(
        parent,
        text=text.upper(),
        font=FONT_SM,
        text_color=TEXT_DIM,
        anchor="w"
    )
    lbl.pack(padx=30, anchor="w", pady=(6, 0))

def make_slider(parent, label, from_, to, initial, on_change, unit="", integer=False):
    frame = ctk.CTkFrame(parent, fg_color="transparent")

    lbl = ctk.CTkLabel(
        frame,
        text=label,
        font=FONT,
        text_color=TEXT_DIM,
        width=60,
        anchor="w"
    )
    lbl.grid(row=0, column=0, padx=(0, 10))

    def format_val(v):
        return f"{int(v)}{unit}" if integer else f"{v:.2f}{unit}"

    val_label = ctk.CTkLabel(
        frame,
        text=format_val(initial),
        font=FONT,
        text_color=TEXT,
        width=55,
        anchor="e"
    )
    val_label.grid(row=0, column=2, padx=(10, 0))

    def on_slider_change(v):
        val_label.configure(text=format_val(v))
        on_change(int(v) if integer else v)

    slider = ctk.CTkSlider(
        frame,
        from_=from_,
        to=to,
        width=260,
        button_color=ACCENT,
        button_hover_color=RED,
        progress_color=ACCENT,
        fg_color=SURFACE,
        command=on_slider_change
    )
    slider.set(initial)
    slider.grid(row=0, column=1)

    return frame, slider


def make_play_button(parent, on_play, on_stop):
    playing = [False]

    def on_click():
        if playing[0]:
            playing[0] = False
            btn.configure(
                text=play,
                fg_color=SURFACE,
                hover_color=ACCENT,
                text_color=TEXT
            )
            on_stop()
        else:
            playing[0] = True
            btn.configure(
                text=stop,
                fg_color=RED,
                hover_color="#8B0000",
                text_color=TEXT
            )
            on_play()

    btn = ctk.CTkButton(
        parent,
        text=play,
        width=180,
        height=40,
        fg_color=SURFACE,
        hover_color=ACCENT,
        text_color=TEXT,
        corner_radius=6,
        font=FONT_BOLD,
        command=on_click
    )

    return btn