import asyncio
import tempfile
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf

from voice_agent import summarize_audio

SAMPLE_RATE = 44100
CHANNELS = 1


def record_from_mic() -> Path:
    frames = []

    def callback(indata, frame_count, time_info, status):
        frames.append(indata.copy())

    audio_path = Path(tempfile.gettempdir()) / "voice_agent_recording.wav"

    print("Recording... press Enter to stop.")
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback):
        input()

    recording = np.concatenate(frames, axis=0)
    sf.write(audio_path, recording, SAMPLE_RATE)
    print(f"Recording saved to {audio_path}")
    return audio_path


if __name__ == "__main__":
    audio_file = record_from_mic()
    asyncio.run(summarize_audio(audio_file))
