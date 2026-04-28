# colours-of-noise 🎵

A lightweight standalone desktop noise machine for focus, studies, work, and sleep. Generates White, Pink, and Brown noise - which are refined from raw waveforms - continuously in real time.

---

## Project Structure

```
colours-of-noise/
├── sound_engine/
│   ├── __init__.py
│   ├── wave_generator.py     # raw numpy signal generation (raw waveforms)
│   └── sound_generator.py    # audio streaming, filters, NoisePlayer class
├── utils/
│   ├── __init__.py
│   ├── ux_controls.py        # reusable widget functions
│   └── dashboard.py          # main window layout with all widgets
├── config.py                 # all constants and defaults in one place
├── app.py                    # entry point
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone https://github.com/Mahraan24/colours-of-noise
cd colours-of-noise
pip install -r requirements.txt
python app.py
```

**Requirements:** Python 3.10+

**Dependencies:** `customtkinter`, `numpy`, `sounddevice`

---

## License

MIT