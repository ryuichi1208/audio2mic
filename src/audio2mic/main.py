#!/usr/bin/env python3
import queue
import sys
import threading
import time
from pathlib import Path

import click
import numpy as np
import pyaudio
import soundfile as sf
from pydub import AudioSegment


class AudioStreamer:
    def __init__(self, file_path: str, device_index: int | None = None, chunk_size: int = 1024):
        self.file_path = Path(file_path)
        self.device_index = device_index
        self.chunk_size = chunk_size
        self.audio_queue = queue.Queue(maxsize=100)
        self.stop_event = threading.Event()
        self.p = pyaudio.PyAudio()

        if not self.file_path.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        self.load_audio()

    def load_audio(self):
        ext = self.file_path.suffix.lower()

        supported_formats = {
            ".mp3": "mp3",
            ".wav": "wav",
            ".ogg": "ogg",
            ".flac": "flac",
            ".m4a": "m4a",
            ".aac": "aac",
            ".wma": "wma",
            ".opus": "opus",
        }

        if ext not in supported_formats:
            raise ValueError(f"Unsupported audio format: {ext}")

        if ext in [".wav", ".flac"]:
            self.audio_data, self.sample_rate = sf.read(str(self.file_path))
            if len(self.audio_data.shape) > 1:
                self.audio_data = np.mean(self.audio_data, axis=1)
            self.audio_data = (self.audio_data * 32767).astype(np.int16)
        else:
            audio = AudioSegment.from_file(str(self.file_path), format=supported_formats[ext])
            audio = audio.set_channels(1)
            self.sample_rate = audio.frame_rate
            samples = np.array(audio.get_array_of_samples())
            self.audio_data = samples.astype(np.int16)

    def list_devices(self):
        click.echo("\nAvailable audio devices:")
        click.echo("-" * 50)
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if info["maxOutputChannels"] > 0:
                default_marker = (
                    " (DEFAULT)" if i == self.p.get_default_output_device_info()["index"] else ""
                )
                click.echo(f"  [{i}] {info['name']}{default_marker}")
                click.echo(
                    f"      Channels: {info['maxOutputChannels']}, Sample Rate: {info['defaultSampleRate']}"
                )

    def producer(self):
        chunk_samples = self.chunk_size
        total_samples = len(self.audio_data)
        position = 0

        while position < total_samples and not self.stop_event.is_set():
            end_pos = min(position + chunk_samples, total_samples)
            chunk = self.audio_data[position:end_pos]

            if len(chunk) < chunk_samples:
                chunk = np.pad(chunk, (0, chunk_samples - len(chunk)), mode="constant")

            try:
                self.audio_queue.put(chunk.tobytes(), timeout=0.1)
            except queue.Full:
                continue

            position = end_pos

        self.audio_queue.put(None)

    def stream_callback(self, in_data, frame_count, time_info, status):  # noqa: ARG002
        try:
            data = self.audio_queue.get_nowait()
            if data is None:
                return (b"\x00" * frame_count * 2, pyaudio.paComplete)
            return (data, pyaudio.paContinue)
        except queue.Empty:
            return (b"\x00" * frame_count * 2, pyaudio.paContinue)

    def stream(self, loop: bool = False):
        stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            output=True,
            output_device_index=self.device_index,
            frames_per_buffer=self.chunk_size,
            stream_callback=self.stream_callback,
        )

        click.echo(f"\nStreaming: {self.file_path.name}")
        click.echo(f"Sample rate: {self.sample_rate} Hz")
        click.echo(f"Duration: {len(self.audio_data) / self.sample_rate:.2f} seconds")
        click.echo("\nPress Ctrl+C to stop streaming...")

        try:
            while True:
                producer_thread = threading.Thread(target=self.producer)
                producer_thread.start()

                producer_thread.join()

                if not loop or self.stop_event.is_set():
                    break

                click.echo("Looping...")
                time.sleep(0.5)

                while not self.audio_queue.empty():
                    self.audio_queue.get()

        except KeyboardInterrupt:
            click.echo("\n\nStopping stream...")
            self.stop_event.set()

        finally:
            stream.stop_stream()
            stream.close()

    def cleanup(self):
        self.p.terminate()


@click.command()
@click.argument("audio_file", type=click.Path(exists=True))
@click.option(
    "--device",
    "-d",
    type=int,
    help="Output device index (use --list-devices to see available devices)",
)
@click.option("--list-devices", "-l", is_flag=True, help="List available audio output devices")
@click.option("--loop", is_flag=True, help="Loop the audio file continuously")
@click.option("--chunk-size", "-c", type=int, default=1024, help="Audio chunk size (default: 1024)")
def cli(audio_file, device, list_devices, loop, chunk_size):
    """
    Stream audio files to microphone/audio output.

    Supports multiple audio formats: MP3, WAV, OGG, FLAC, M4A, AAC, WMA, OPUS

    Examples:
        audio2mic song.mp3
        audio2mic podcast.wav --loop
        audio2mic voice.flac --device 2
    """
    try:
        streamer = AudioStreamer(audio_file, device, chunk_size)

        if list_devices:
            streamer.list_devices()
            sys.exit(0)

        streamer.stream(loop=loop)

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)
    finally:
        if "streamer" in locals():
            streamer.cleanup()


if __name__ == "__main__":
    cli()
