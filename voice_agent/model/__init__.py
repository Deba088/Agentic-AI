from pathlib import Path

from agents import Agent
from openai import OpenAI

MODEL_NAME = "gpt-5.4-nano"
VOICE_MODEL_NAME = "whisper-1"


def transcribe_audio(audio_path: str | Path, client: OpenAI | None = None) -> str:
    """Transcribe an audio file to text using OpenAI's Whisper model."""
    client = client or OpenAI()
    audio_path = Path(audio_path)

    with audio_path.open("rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=VOICE_MODEL_NAME,
            file=audio_file,
        )

    return transcription.text


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
