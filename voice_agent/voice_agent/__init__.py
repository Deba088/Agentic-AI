import asyncio
from pathlib import Path

from agents import Runner, trace
from openai.types.responses import ResponseTextDeltaEvent

from model import create_summary_agent, transcribe_audio


async def summarize_audio(audio_path: str | Path) -> None:
    transcript = transcribe_audio(audio_path)
    print(transcript)
    print("\n\n")

    summary_agent = create_summary_agent()
    with trace("Voice agent workflow"):
        result = Runner.run_streamed(summary_agent, transcript)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    audio_file = input("Enter path to audio file: ")
    asyncio.run(summarize_audio(audio_file))
