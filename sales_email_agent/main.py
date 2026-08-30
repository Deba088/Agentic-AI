from dotenv import load_dotenv
from agents import Runner, trace
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
from sales_agents import sales_agent

load_dotenv(override=True)
MODEL_NAME = "gpt-5.4-nano"


async def main():
    message = "Send a sales email"

    with trace("Sales email workflow"):
        results = await Runner.run(sales_agent, message)
        print(results.final_output)

    with trace("Sales email workflow"):
        results = Runner.run_streamed(sales_agent, message)
        async for event in results.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
