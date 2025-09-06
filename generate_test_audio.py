#!/usr/bin/env python3

import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
from scipy import signal


def create_test_audio():
    print("Generating test audio files...")

    # 1. Simple tone (440Hz A note)
    print("Creating test_tone.wav - 440Hz sine wave (3 seconds)")
    tone = Sine(440).to_audio_segment(duration=3000)
    tone.export("test_tone.wav", format="wav")

    # 2. Beep pattern
    print("Creating test_beeps.wav - Beep pattern")
    beep = Sine(800).to_audio_segment(duration=200)
    silence = AudioSegment.silent(duration=300)
    pattern = beep + silence + beep + silence + beep + AudioSegment.silent(duration=1000)
    pattern = pattern * 2  # Repeat twice
    pattern.export("test_beeps.wav", format="wav")

    # 3. Sweep frequency
    print("Creating test_sweep.wav - Frequency sweep (100Hz to 2000Hz)")
    duration = 5
    sample_rate = 44100
    t = np.linspace(0, duration, sample_rate * duration)

    # Logarithmic sweep
    f0 = 100
    f1 = 2000
    sweep = signal.chirp(t, f0, duration, f1, method="logarithmic")

    # Convert to 16-bit PCM
    sweep = np.int16(sweep * 32767 * 0.5)  # 50% volume

    # Create AudioSegment from numpy array
    audio = AudioSegment(sweep.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1)
    audio.export("test_sweep.wav", format="wav")

    # 4. Multi-tone test
    print("Creating test_music.wav - Simple melody")
    notes = [
        (440, 500),  # A
        (494, 500),  # B
        (523, 500),  # C
        (587, 500),  # D
        (659, 500),  # E
        (587, 500),  # D
        (523, 500),  # C
        (494, 500),  # B
        (440, 1000),  # A (long)
    ]

    melody = AudioSegment.empty()
    for freq, duration in notes:
        note = Sine(freq).to_audio_segment(duration=duration)
        # Add fade in/out for smoother sound
        note = note.fade_in(50).fade_out(50)
        melody += note

    melody.export("test_music.wav", format="wav")

    # 5. Voice-like test (using modulated tones)
    print("Creating test_voice.wav - Modulated tones (voice-like)")
    duration = 3
    t = np.linspace(0, duration, sample_rate * duration)

    # Base frequency with vibrato
    base_freq = 200
    vibrato_freq = 5
    vibrato_depth = 10

    frequency = base_freq + vibrato_depth * np.sin(2 * np.pi * vibrato_freq * t)
    phase = 2 * np.pi * np.cumsum(frequency) / sample_rate
    voice = np.sin(phase)

    # Add harmonics
    voice += 0.3 * np.sin(2 * phase)  # 2nd harmonic
    voice += 0.2 * np.sin(3 * phase)  # 3rd harmonic

    # Apply envelope
    envelope = np.exp(-t * 0.5) * (1 - np.exp(-t * 10))
    voice = voice * envelope

    # Normalize and convert
    voice = voice / np.max(np.abs(voice))
    voice = np.int16(voice * 32767 * 0.7)

    audio = AudioSegment(voice.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1)
    audio.export("test_voice.wav", format="wav")

    print("\nTest audio files created:")
    print("  - test_tone.wav    : Simple 440Hz tone")
    print("  - test_beeps.wav   : Beep pattern for testing")
    print("  - test_sweep.wav   : Frequency sweep")
    print("  - test_music.wav   : Simple melody")
    print("  - test_voice.wav   : Voice-like modulated sound")


if __name__ == "__main__":
    create_test_audio()
