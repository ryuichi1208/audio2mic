# audio2mic

Stream audio files directly to your microphone/audio output device. Perfect for playing audio files through virtual audio cables, streaming audio in voice chats, or testing audio applications.

## Features

- **Multiple Format Support**: MP3, WAV, OGG, FLAC, M4A, AAC, WMA, OPUS
- **Device Selection**: Choose specific audio output devices
- **Loop Playback**: Continuously loop audio files
- **Real-time Streaming**: Low-latency audio streaming
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/ryuichi1208/audio2mic.git
cd audio2mic

# Install with uv
uv sync

# Run the tool
uv run audio2mic --help
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/ryuichi1208/audio2mic.git
cd audio2mic

# Install dependencies
pip install -e .
```

## Usage

### Basic Usage

Stream an audio file to the default output device:

```bash
audio2mic audio.mp3
```

### List Available Devices

View all available audio output devices:

```bash
audio2mic audio.mp3 --list-devices
```

### Select Specific Device

Stream to a specific device by its index:

```bash
audio2mic audio.mp3 --device 2
```

### Loop Playback

Continuously loop the audio file:

```bash
audio2mic audio.mp3 --loop
```

### Advanced Options

Adjust chunk size for performance tuning:

```bash
audio2mic audio.mp3 --chunk-size 2048
```

## Command Line Options

```
Usage: audio2mic [OPTIONS] AUDIO_FILE

Options:
  -d, --device INTEGER     Output device index
  -l, --list-devices       List available audio output devices
  --loop                   Loop the audio file continuously
  -c, --chunk-size INTEGER Audio chunk size (default: 1024)
  --help                   Show this message and exit
```

## Supported Audio Formats

- **MP3** - MPEG Audio Layer III
- **WAV** - Waveform Audio File Format
- **OGG** - Ogg Vorbis
- **FLAC** - Free Lossless Audio Codec
- **M4A** - MPEG-4 Audio
- **AAC** - Advanced Audio Coding
- **WMA** - Windows Media Audio
- **OPUS** - Opus Audio Codec

## Use Cases

### Virtual Audio Cable

Stream audio through virtual audio cables for:
- Discord, Teams, Zoom voice chats
- OBS Studio audio sources
- Audio routing between applications

### Testing

- Test audio processing applications
- Verify audio device functionality
- Benchmark audio streaming performance

### Broadcasting

- Play sound effects in live streams
- Queue music for radio shows
- Automate audio playback

## System Requirements

- Python 3.12 or higher
- PyAudio (requires system audio libraries)
  - Windows: No additional requirements
  - macOS: `brew install portaudio`
  - Linux: `sudo apt-get install portaudio19-dev`

## Troubleshooting

### PyAudio Installation Issues

If you encounter issues installing PyAudio:

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Ubuntu/Debian:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**Windows:**
```bash
# Use pre-built wheels
pip install pipwin
pipwin install pyaudio
```

### Permission Issues

On macOS, you may need to grant microphone/audio permissions to your terminal application.

### Device Not Found

If your desired device doesn't appear in the list:
1. Ensure the device is connected and enabled
2. Restart the audio service
3. Check system audio settings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Author

ryuichi1208

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI interface
- Audio processing powered by [PyDub](https://github.com/jiaaro/pydub) and [SoundFile](https://python-soundfile.readthedocs.io/)
- Streaming capabilities via [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)