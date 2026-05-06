import customtkinter as ctk
import tkinter as tk

#Colours
BG       = "#F4F1BB"   # lemon chiffon - background
SURFACE  = "#9BC1BC"   # ash grey - btn
ACCENT   = "#ED6A5A"   # vibrant coral - hover
RED      = "#BD1E1E"   # deep red - play/stop
TEXT     = "#2D2D2D"   # near black — readable text
TEXT_DIM = "#5CA4A9"   # tropical teal — labels
DIVIDER  = "#5CA4A9"   # tropical teal — dividers
FONT     = ("Comic Sans MS", 11)
FONT_BOLD= ("Comic Sans MS", 11, "bold")
FONT_SM  = ("Comic Sans MS", 9)

PRESETS = {
    "Rain": dict(white=0.0, pink=0.0, brown=0.0, volume=0.00, timer=0),
    "Ocean": dict(white=0.0, pink=0.0, brown=0.0, volume=0.00, timer=60),
    "Wind": dict(white=0.0, pink=0.0, brown=0.0, volume=0.00, timer=0),
    "Fireplace": dict(white=0.0, pink=0.0, brown=0.0, volume=0.00, timer=0),
}

app = ctk.CTk()
app.geometry("720x450")
app.configure(fg_color=BG)

def create_button(text, x, y):
    button = ctk.CTkButton(
        master=app,
        text=text,
        fg_color=SURFACE,
        hover_color=ACCENT,
        text_color=TEXT,
    )
    button.place(relx=x, rely=y, anchor="center")

def play_button():
    pass

def create_slider():
    pass


def radiobutton_event():
    print("radiobutton toggled, current value:", radio_var.get())

radio_var = tk.IntVar(value=0)
radiobutton_1 = ctk.CTkRadioButton(app, text="CTkRadioButton 1", command=radiobutton_event, variable= radio_var, value=1)
radiobutton_2 = ctk.CTkRadioButton(app, text="CTkRadioButton 2", command=radiobutton_event, variable= radio_var, value=2)

plc=0.15
for opt in PRESETS.keys():
    create_button(opt,x=plc,y=0.10)
    plc+=0.20

app.mainloop()