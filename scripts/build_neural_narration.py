import asyncio
import edge_tts
import subprocess
from pathlib import Path
import wave
import struct

OUT = Path("demo_out")
OUT.mkdir(exist_ok=True)

VOICE = "en-US-ChristopherNeural"
SAMPLE_RATE = 24000

SCENES_DEF = [
    {
        "id": "act1_hook",
        "title": "Act I - The Consensus Illusion",
        "type": "neural",
        "text": "Ask standard AI a contested scientific question, and it gives you a smooth, polite answer. But real research does not have a single consensus. It has opposing data, conflicting clinical trials, and sharp debate. When AI flattens that tension into a one-sided summary, it hides the truth.",
    },
    {
        "id": "act2_title",
        "title": "Act II - The Invention",
        "type": "composite_user",
        "part_a": "All Vibes presents: Research Courtroom. Created and engineered by...",
        "user_wav": "demo_out/user_voice.wav",
        "part_c": "...for the Nebius Hackathon. We replace polite summarization with an adversarial trial: a Prosecution, a Defense, and an impartial Judge.",
        "text": "All Vibes presents Research Courtroom. Created and engineered by Pramodh Nanjayya for the Nebius Hackathon. We replace polite summarization with an adversarial trial: a Prosecution, a Defense, and an impartial Judge.",
    },
    {
        "id": "act2_stream",
        "title": "Act II - Live Deliberation Stream",
        "type": "neural",
        "text": "I file a real contested question: does intermittent fasting improve long-term weight loss compared with calorie restriction? Watch the live deliberation feed. Tavily searches real-time sources, hashes each excerpt, and seals the evidence ledger.",
    },
    {
        "id": "act2_arguments",
        "title": "Act II - Opposing Counsel & Verification",
        "type": "neural",
        "text": "The document drafts live. The Prosecution argues the affirmative case from admitted evidence. The Defense counters with trial duration limits and protocol heterogeneity. Every claim is audited by a separate Nebius Qwen reasoner call that verifies whether the excerpt actually supports the claim.",
    },
    {
        "id": "act2_cross_exam",
        "title": "Act II - Cross-Examination",
        "type": "neural",
        "text": "Counsel then cross-examine each other directly on evidence veracity. Notice the citations: hallucinated source IDs are stripped instantly. If evidence cannot be verified, the court is forced by code to rule inconclusive.",
    },
    {
        "id": "act2_verdict_popup",
        "title": "Act II - The Verdict Pop-Up",
        "type": "neural",
        "text": "The verdict is reached. An instant ruling announcement confirms the finding: inconclusive for long-term superiority, with comparable 12-month outcomes. We review the full judicial reasoning, findings matrix, and unresolved questions.",
    },
    {
        "id": "act3_reconsideration",
        "title": "Act III - Interactive Challenge & SSRF Defense",
        "type": "neural",
        "text": "Now, we cross-examine the court. When I challenge with a blocked cloud metadata address, hardened SSRF protections refuse the socket cold. And when I introduce genuine evidence, the court tracks revisions without flipping arbitrarily.",
    },
    {
        "id": "act3_conclusion",
        "title": "Act III - The Future is Already Running",
        "type": "neural",
        "text": "Fifty-six automated tests. Full-stack SSE streaming. Zero fabricated citations. Research Courtroom proves that the future of AI research is not about confident summaries. It is about verifiable truth.",
    },
]

async def generate_speech_clip(text: str, out_wav: Path, rate: str = "-4%"):
    out_mp3 = out_wav.with_suffix(".mp3")
    comm = edge_tts.Communicate(text, VOICE, rate=rate)
    await comm.save(str(out_mp3))
    subprocess.run([
        "ffmpeg", "-y", "-i", str(out_mp3),
        "-ar", str(SAMPLE_RATE), "-ac", "1",
        str(out_wav)
    ], check=True, capture_output=True)

def normalize_wav(in_wav: Path, out_wav: Path, target_peak: int = 28000):
    with wave.open(str(in_wav), "rb") as w:
        n = w.getnframes()
        sw = w.getsampwidth()
        raw = w.readframes(n)
        samples = struct.unpack(f"<{n}h", raw)
    
    max_val = max(abs(s) for s in samples) or 1
    gain = target_peak / max_val
    normalized = [max(-32767, min(32767, int(s * gain))) for s in samples]
    
    with wave.open(str(out_wav), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(struct.pack(f"<{n}h", *normalized))

async def assemble_all_clips():
    print("🎙️ Generating Neural Voice clips + splicing User's Voice...")
    results = {}
    for sc in SCENES_DEF:
        sid = sc["id"]
        out_final = OUT / f"{sid}_neural.wav"
        
        if sc["type"] == "neural":
            await generate_speech_clip(sc["text"], out_final)
            normalize_wav(out_final, out_final)
        elif sc["type"] == "composite_user":
            part_a_wav = OUT / "act2_part_a.wav"
            part_c_wav = OUT / "act2_part_c.wav"
            user_clean_wav = OUT / "user_voice_clean.wav"
            
            await generate_speech_clip(sc["part_a"], part_a_wav, rate="-2%")
            await generate_speech_clip(sc["part_c"], part_c_wav, rate="-4%")
            
            # Prepare user voice at 24000Hz mono and normalize
            subprocess.run([
                "ffmpeg", "-y", "-i", sc["user_wav"],
                "-ar", str(SAMPLE_RATE), "-ac", "1",
                str(user_clean_wav)
            ], check=True, capture_output=True)
            normalize_wav(user_clean_wav, user_clean_wav, target_peak=28000)
            
            # Create a 0.3s pause silence
            silence_samples = int(SAMPLE_RATE * 0.3)
            silence_bytes = struct.pack(f"<{silence_samples}h", *([0] * silence_samples))
            
            # Read all 3 parts and concatenate
            combined_samples = []
            for p, add_pause in [(part_a_wav, True), (user_clean_wav, True), (part_c_wav, False)]:
                with wave.open(str(p), "rb") as w:
                    n = w.getnframes()
                    raw = w.readframes(n)
                    combined_samples.extend(struct.unpack(f"<{n}h", raw))
                if add_pause:
                    combined_samples.extend([0] * silence_samples)
                    
            with wave.open(str(out_final), "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(SAMPLE_RATE)
                w.writeframes(struct.pack(f"<{len(combined_samples)}h", *combined_samples))
                
        with wave.open(str(out_final), "rb") as w:
            dur = w.getnframes() / w.getframerate()
        results[sid] = (out_final, dur)
        print(f"  • {sc['title']}: {dur:.2f}s -> {out_final}")

    return results

if __name__ == "__main__":
    asyncio.run(assemble_all_clips())
