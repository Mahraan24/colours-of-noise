from sound_engine.sound_generator import NoisePlayer
import time

def test_play_default():
    """Plays default noise (in config.py) for 5 seconds."""
    print("test_play_default: playing...")
    player = NoisePlayer()
    player.play()
    time.sleep(5)
    player.stop()
    print("test_play_default ✓\n")

def test_blend_switch():
    """Cycles through white, pink and brown one at a time."""
    print("test_blend_switch: switching white -> pink -> brown...")
    player = NoisePlayer()
    player.play()

    player.set_blend(white=1, pink=0, brown=0)
    print("  white...")
    time.sleep(4)

    player.set_blend(white=0, pink=1, brown=0)
    print("  pink...")
    time.sleep(4)

    player.set_blend(white=0, pink=0, brown=1)
    print("  brown...")
    time.sleep(4)

    player.stop()
    print("test_blend_switch ✓\n")

def test_blend_mix():
    """Plays an equal mix of all three noises."""
    print("test_blend_mix: equal mix...")
    player = NoisePlayer()
    player.set_blend(white=1, pink=1, brown=1)
    player.play()
    time.sleep(5)
    player.stop()
    print("test_blend_mix ✓\n")

def test_volume():
    """Ramps volume from low to high."""
    print("test_volume: ramping 0.2 -> 1.0...")
    player = NoisePlayer()
    player.play()
    for v in [0.2, 0.4, 0.6, 0.8, 1.0]:
        player.set_volume(v)
        print(f"  volume: {v}")
        time.sleep(2)
    player.stop()
    print("test_volume ✓\n")

def test_timer():
    """Sets a 10s timer with fade out over last 5s."""
    print("test_timer: 10s timer, 5s fade...")
    player = NoisePlayer()
    player.set_timer(10)
    player.play()
    time.sleep(12)  # wait a bit longer than timer
    player.stop()
    print("test_timer ✓\n")

if __name__ == "__main__":
    test_play_default()
    test_blend_switch()
    test_blend_mix()
    test_volume()
    test_timer()