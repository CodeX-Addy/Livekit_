import asyncio
from api import AssistantFnc
from dotenv import load_dotenv
from livekit.plugins import openai, silero
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm

load_dotenv()

## Entrypoint for agentic assistant
async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be only voice."
            "You should use brief and concise responses, and avoiding usage of unpronouncable punctuation."
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_ctx = AssistantFnc()

    assitant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx,
    )
    assitant.start(ctx.room)
    await asyncio.sleep(1)
    await assitant.say("Hey, How Can I Help You Today!", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
