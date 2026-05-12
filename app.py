from sound_engine.sound_generator import NoisePlayer
from view.dashboard import Dashboard

def main():
    player = NoisePlayer()

    app = Dashboard(
        on_play   = player.play,
        on_stop   = player.stop,
        on_volume = player.set_volume,
        on_blend  = player.set_blend,
        on_timer  = player.set_timer,
    )

    app.mainloop()

if __name__ == "__main__":
    main()