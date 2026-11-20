import asyncio
import edge_tts
import subprocess
from pathlib import Path
import wave

OUT = Path("demo_out")
OUT.mkdir(exist_ok=True)

VOICE = "en-US-ChristopherNeural"

async def generate_neural(text: str, out_wav: Path):
    out_mp3 = out_wav.with_suffix(".mp3")
    comm = edge_tts.Communicate(text, VOICE, rate="-4%")
    await comm.save(str(out_mp3))
    subprocess.run(["ffmpeg", "-y", "-i", str(out_mp3), "-ar", "24000", "-ac", "1", str(out_wav)], check=True, capture_output=True)
    with wave.open(str(out_wav), "rb") as w:
        dur = w.getnframes() / w.getframerate()
    return dur

async def main():
    text = (
        "Ask standard AI a contested scientific question, and it gives you a smooth, polite answer. "
        "But real research does not have a single consensus. It has opposing data, conflicting clinical trials, "
        "and sharp debate. When AI flattens that tension into a one-sided summary, it hides the truth."
    )
    wav_p = OUT / "test_neural_act1.wav"
    dur = await generate_neural(text, wav_p)
    print(f"Generated {wav_p} ({dur:.2f}s) with natural neural voice!")

if __name__ == "__main__":
    asyncio.run(main())
