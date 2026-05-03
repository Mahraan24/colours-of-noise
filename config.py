# Audio
buffer_size = 4096       # samples per callback (~93ms at 44100Hz)
samplerate = 44100       # Hz

# Blend defaults
white_weight = 1.0
pink_weight = 0.0
brown_weight = 0.0

# Playback defaults
volume = 0.7             # 0.0 to 1.0
timer = None             # seconds, None = no timer

# Fade out
fade_duration = 60       # seconds before timer expiry to begin gradual fade