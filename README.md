# audio2mic

音声をマイクに流し込むやつ

``` usage
Usage: audio2mic [OPTIONS] AUDIO_FILE

  Stream audio files to microphone/audio output.

  Supports multiple audio formats: MP3, WAV, OGG, FLAC, M4A, AAC, WMA, OPUS

  Examples:     audio2mic song.mp3     audio2mic podcast.wav --loop
  audio2mic voice.flac --device 2

Options:
  -d, --device INTEGER      Output device index (use --list-devices to see
                            available devices)
  -l, --list-devices        List available audio output devices
  --loop                    Loop the audio file continuously
  -c, --chunk-size INTEGER  Audio chunk size (default: 1024)
  --help                    Show this message and exit.
```

