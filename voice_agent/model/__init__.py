import io
import math
from pathlib import Path

import soundfile as sf
from agents import Agent
from openai import OpenAI

MODEL_NAME = "gpt-5.4-nano"
VOICE_MODEL_NAME = "whisper-1"
MAX_CHUNK_BYTES = 20 * 1024 * 1024  # 20MB, safely under OpenAI's 25MB limit


def _chunk_audio(audio_path: Path) -> list[bytes]:
    """Split an audio file into WAV byte chunks no larger than MAX_CHUNK_BYTES."""
    data, samplerate = sf.read(audio_path, dtype="int16")
    channels = 1 if data.ndim == 1 else data.shape[1]
    bytes_per_frame = data.itemsize * channels

    total_bytes = data.shape[0] * bytes_per_frame
    if total_bytes <= MAX_CHUNK_BYTES:
        buffer = io.BytesIO()
        sf.write(buffer, data, samplerate, format="WAV")
        return [buffer.getvalue()]

    num_chunks = math.ceil(total_bytes / MAX_CHUNK_BYTES)
    frames_per_chunk = math.ceil(data.shape[0] / num_chunks)

    chunks = []
    for start in range(0, data.shape[0], frames_per_chunk):
        chunk_data = data[start : start + frames_per_chunk]
        buffer = io.BytesIO()
        sf.write(buffer, chunk_data, samplerate, format="WAV")
        chunks.append(buffer.getvalue())

    return chunks


def transcribe_audio(audio_path: str | Path, client: OpenAI | None = None) -> str:
    """Transcribe an audio file to text using OpenAI's Whisper model.

    Splits the audio into <=20MB chunks before sending, since the Whisper API
    rejects files larger than 25MB.
    """
    client = client or OpenAI()
    audio_path = Path(audio_path)

    chunks = _chunk_audio(audio_path)

    transcripts = []
    for index, chunk_bytes in enumerate(chunks):
        chunk_file = io.BytesIO(chunk_bytes)
        chunk_file.name = f"{audio_path.stem}_chunk{index}.wav"
        transcription = client.audio.transcriptions.create(
            model=VOICE_MODEL_NAME,
            file=chunk_file,
        )
        transcripts.append(transcription.text)

    return " ".join(transcripts)


def create_summary_agent() -> Agent:
    instructions = """
    You are a summary agent.
    Your task is to generate a summary from the audio transription.
    Analysed the fundamental things discussed in the meeting.
    What a user should take note into account.
    What is the next step mentioned.
    """.strip()

    summary_agent = Agent(name="summary_agent", instructions=instructions, model=MODEL_NAME)
    return summary_agent
