import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sound_engine.wave_generator import Wave

def power_spectrum(wave, sample_rate=44100):
    fft = np.fft.rfft(wave)
    power = np.abs(fft) ** 2
    freqs = np.fft.rfftfreq(len(wave), d=1 / sample_rate)
    return freqs, power

def plot_all():
    w = Wave()
    noises = [
        (w.white(), "White", "#4A90D9"),
        (w.pink(),  "Pink",  "#E0729A"),
        (w.brown(), "Brown", "#A0622A"),
    ]

    fig, axes = plt.subplots(3, 2, figsize=(12, 8))

    for row, (wave, label, colour) in enumerate(noises):
        freqs, power = power_spectrum(wave)

        # time domain
        axes[row, 0].plot(wave, color=colour, linewidth=0.5)
        axes[row, 0].set_ylim(-1.1, 1.1)
        axes[row, 0].set_ylabel(label, fontsize=10)
        axes[row, 0].set_xticks([])
        axes[row, 0].set_yticks([])

        # frequency domain
        axes[row, 1].loglog(freqs[1:], power[1:], color=colour, linewidth=0.8)
        axes[row, 1].set_xticks([])
        axes[row, 1].set_yticks([])

    axes[0, 0].set_title("time", fontsize=10, color="gray")
    axes[0, 1].set_title("frequency", fontsize=10, color="gray")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_all()