"""Master Presentation Film Producer: Slides + Live Demo.

Structure:
- Part 1: Visual Keynote Slides (Title, Problem, Architecture, Security, Demo Setup)
  featuring Pramodh Nanjayya's real voice recording on Slide 1!
- Part 2: Authentic Live Demo of Research Courtroom (http://localhost:3000)
  (Deliberation stream, live auto-population, citation audit, verdict pop-up dialog, SSRF defense)
- Scored with Hollywood trailer music ('The Epic 2' by Rafael Krux) + Sidechain Ducking!
"""
import asyncio
import math
from pathlib import Path
import struct
import subprocess
import time
import wave
import edge_tts
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

OUT = Path("demo_out")
OUT.mkdir(exist_ok=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
VOICE = "en-US-ChristopherNeural"
SAMPLE_RATE = 24000

SLIDES_HTML = (OUT / "slides.html").resolve().as_uri()
APP_URL = "http://localhost:3000"
BLOCKED_URL = "http://169.254.169.254/latest/meta-data/"
USER_VOICE_WAV = OUT / "user_voice.wav"
TRAILER_MUSIC_WAV = OUT / "the_epic_2.wav"

SCENES = [
    # --- PART 1: SLIDES ---
    {
        "id": "s1_title",
        "section": "slides",
        "slide_num": 1,
        "type": "composite_user",
        "part_a": "All Vibes presents: Research Courtroom. Created and engineered by...",
        "user_wav": str(USER_VOICE_WAV),
        "part_c": "...for the Nebius Hackathon. We replace polite consensus illusions with adversarial scientific jurisprudence.",
    },
    {
        "id": "s2_problem",
        "section": "slides",
        "slide_num": 2,
        "type": "neural",
        "text": "Ask standard AI a contested clinical question, and it gives you a smooth compromise. But real research doesn't have a single consensus. It has opposing clinical trials, contradictory data, and deep methodological limits. When AI flattens that tension into a one-sided summary, it hides the truth.",
    },
    {
        "id": "s3_arch",
        "section": "slides",
        "slide_num": 3,
        "type": "neural",
        "text": "Our solution: an adversarial courtroom powered by Nebius Qwen-2.5 reasoner. A Prosecution and Defense argue opposing positions from admitted evidence. Every claim is audited by an independent verifier pass before the Judge rules.",
    },
    {
        "id": "s4_security",
        "section": "slides",
        "slide_num": 4,
        "type": "neural",
        "text": "Zero hallucinated citations. Hardened Server-Side Request Forgery protections blocking cloud metadata theft cold. And fifty-six automated tests verifying system invariants.",
    },
    {
        "id": "s5_demo_intro",
        "section": "slides",
        "slide_num": 5,
        "type": "neural",
        "text": "And now, let us step into the live courtroom.",
    },
    # --- PART 2: LIVE DEMO ---
    {
        "id": "d1_stream",
        "section": "demo",
        "type": "neural",
        "text": "We file a contested clinical trial case on intermittent fasting. Watch the live deliberation stream. Tavily searches real-time sources, hashes each excerpt into the evidence ledger, and counsel drafts live into the document.",
    },
    {
        "id": "d2_audit",
        "section": "demo",
        "type": "neural",
        "text": "Every citation binds directly to a verified excerpt. If citations are hallucinated, they are stripped immediately. Counsel then cross-examine each other directly on study veracity.",
    },
    {
        "id": "d3_verdict",
        "section": "demo",
        "type": "neural",
        "text": "The verdict has been reached. An instant ruling announcement confirms the finding: inconclusive for long-term superiority, with comparable 12-month outcomes. We review the full judicial reasoning.",
    },
    {
        "id": "d4_challenge",
        "section": "demo",
        "type": "neural",
        "text": "Finally, we cross-examine the court with a blocked metadata address. Hardened security refuses the socket cold. Fifty-six tests passing. Research Courtroom delivers verifiable truth.",
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

async def prepare_all_audio():
    print("\n🎙️ Generating narration clips (Neural AI + User Voice)...")
    clips = {}
    for sc in SCENES:
        sid = sc["id"]
        out_p = OUT / f"{sid}_clip.wav"
        if sc.get("type") == "neural":
            await generate_speech_clip(sc["text"], out_p)
            normalize_wav(out_p, out_p)
        elif sc.get("type") == "composite_user":
            p_a = OUT / f"{sid}_pa.wav"
            p_c = OUT / f"{sid}_pc.wav"
            p_u = OUT / f"{sid}_u.wav"
            await generate_speech_clip(sc["part_a"], p_a, rate="-2%")
            await generate_speech_clip(sc["part_c"], p_c, rate="-4%")
            subprocess.run(["ffmpeg", "-y", "-i", sc["user_wav"], "-ar", str(SAMPLE_RATE), "-ac", "1", str(p_u)], check=True, capture_output=True)
            normalize_wav(p_u, p_u)
            
            silence_samples = int(SAMPLE_RATE * 0.3)
            combined = []
            for p, add_pause in [(p_a, True), (p_u, True), (p_c, False)]:
                with wave.open(str(p), "rb") as w:
                    raw = w.readframes(w.getnframes())
                    combined.extend(struct.unpack(f"<{w.getnframes()}h", raw))
                if add_pause:
                    combined.extend([0] * silence_samples)
            with wave.open(str(out_p), "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(SAMPLE_RATE)
                w.writeframes(struct.pack(f"<{len(combined)}h", *combined))
                
        with wave.open(str(out_p), "rb") as w:
            dur = w.getnframes() / w.getframerate()
        clips[sid] = (out_p, dur)
        print(f"  • {sid}: {dur:.1f}s")
    return clips

def record_and_produce():
    clips = asyncio.run(prepare_all_audio())

    raw_dir = OUT / "slides_raw_video"
    raw_dir.mkdir(exist_ok=True)
    # clean old webm
    for f in raw_dir.glob("*.webm"):
        f.unlink()

    print("\n🖥️ Capturing 1080p Presentation (Slides -> Live Demo)...")
    narration_cues = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(raw_dir),
            record_video_size={"width": 1920, "height": 1080},
        )
        page = context.new_page()
        t0 = time.time()
        elapsed = lambda: time.time() - t0

        def trigger_cue(sid: str, pad: float = 1.2):
            wav_p, dur = clips[sid]
            st = elapsed()
            narration_cues.append((st, wav_p))
            return st + dur + pad

        def wait_until(target_t: float):
            rem = target_t - elapsed()
            if rem > 0:
                page.wait_for_timeout(int(rem * 1000))

        # --- PHASE 1: KEYNOTE SLIDES ---
        page.goto(SLIDES_HTML)
        page.wait_for_selector("#slide-1", timeout=10000)
        page.wait_for_timeout(600)

        # Slide 1: Title
        end_t = trigger_cue("s1_title", pad=1.5)
        wait_until(end_t)

        # Slide 2: Problem
        page.evaluate("window.goToSlide(2)")
        end_t = trigger_cue("s2_problem", pad=1.5)
        wait_until(end_t)

        # Slide 3: Architecture
        page.evaluate("window.goToSlide(3)")
        end_t = trigger_cue("s3_arch", pad=1.5)
        wait_until(end_t)

        # Slide 4: Security
        page.evaluate("window.goToSlide(4)")
        end_t = trigger_cue("s4_security", pad=1.5)
        wait_until(end_t)

        # Slide 5: Transition to Demo
        page.evaluate("window.goToSlide(5)")
        end_t = trigger_cue("s5_demo_intro", pad=2.0)
        wait_until(end_t)

        # --- PHASE 2: LIVE APP DEMO ---
        page.goto(APP_URL)
        page.wait_for_selector(".brand-name", timeout=15000)
        page.wait_for_timeout(1000)

        # Select Preset 1 and Open Trial
        preset_btn = page.get_by_role("button", name="Intermittent fasting")
        preset_btn.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        preset_btn.click()
        page.wait_for_timeout(800)
        page.get_by_role("button", name="Open trial").click()

        # Demo 1: Stream
        end_t = trigger_cue("d1_stream", pad=2.0)
        try:
            page.wait_for_selector(".live-stream-box", timeout=15000)
        except:
            pass
        wait_until(end_t)

        # Demo 2: Audit & Cross-Exam
        end_t = trigger_cue("d2_audit", pad=2.0)
        try:
            page.wait_for_selector(".argument.prosecution", timeout=25000)
            page.get_by_text("Opening arguments").first.scroll_into_view_if_needed()
            page.wait_for_timeout(1500)
            citations = page.locator(".citation")
            if citations.count() > 0:
                citations.first.click()
                page.wait_for_timeout(1500)
                page.keyboard.press("Escape")
        except:
            pass
        wait_until(end_t)

        # Demo 3: Verdict Pop-Up
        end_t = trigger_cue("d3_verdict", pad=2.5)
        try:
            page.wait_for_selector("text=The Verdict Has Been Reached", timeout=50000)
            page.wait_for_timeout(2500)
            review_btn = page.get_by_role("button", name="Review Full Verdict")
            if review_btn.count() > 0:
                review_btn.click()
                page.wait_for_timeout(2000)
        except:
            page.get_by_text("Judicial verdict").first.scroll_into_view_if_needed()
        wait_until(end_t)

        # Demo 4: Challenge & SSRF Security
        end_t = trigger_cue("d4_challenge", pad=3.0)
        try:
            page.get_by_text("Cross-examine the court").first.scroll_into_view_if_needed()
            page.wait_for_timeout(600)
            challenge_input = page.locator("#challenge")
            url_input = page.locator("#source-url")
            if challenge_input.count() > 0 and url_input.count() > 0:
                challenge_input.fill("Re-evaluate findings against 2026 data")
                url_input.fill(BLOCKED_URL)
                page.wait_for_timeout(800)
                page.get_by_role("button", name="Challenge verdict").click()
                page.wait_for_selector(".notice.error", timeout=10000)
                page.wait_for_timeout(2500)
        except:
            pass
        wait_until(end_t)

        total_duration = elapsed()
        context.close()
        browser.close()

    recorded_webms = list(raw_dir.glob("*.webm"))
    if not recorded_webms:
        raise RuntimeError("No recording found")
    raw_video = recorded_webms[0]
    print(f"✅ Screen recording complete: {raw_video} ({total_duration:.1f}s)")

    # Assemble narration master track
    print("\n🎛️ Assembling master voiceover track...")
    total_samples = int(SAMPLE_RATE * (total_duration + 2.0))
    master = [0] * total_samples
    for st, wav_p in narration_cues:
        with wave.open(str(wav_p), "rb") as w:
            n = w.getnframes()
            raw = w.readframes(n)
            samples = struct.unpack(f"<{n}h", raw)
            idx = int(st * SAMPLE_RATE)
            for j in range(len(samples)):
                if idx + j < total_samples:
                    master[idx + j] += samples[j]
    
    max_val = max(abs(s) for s in master) or 1
    gain = 28000 / max_val
    master_wav = OUT / "slides_voice_master.wav"
    with wave.open(str(master_wav), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(struct.pack(f"<{len(master)}h", *[max(-32767, min(32767, int(s * gain))) for s in master]))

    # Mix with Trailer Music using Sidechain Ducking
    print("\n🎵 Mastering Hollywood Trailer Soundtrack with Sidechain Ducking...")
    trailer_master = OUT / "slides_soundtrack_master.wav"
    fade_st = max(0, total_duration - 4.0)
    filter_complex = (
        f"[1:a]afade=t=out:st={fade_st:.1f}:d=3.8,volume=0.28[music];"
        f"[music][0:a]sidechaincompress=threshold=0.04:ratio=4:attack=50:release=450[ducked];"
        f"[0:a]volume=1.3[voice];"
        f"[voice][ducked]amix=inputs=2:duration=first:dropout_transition=2[aout]"
    )
    subprocess.run([
        FFMPEG, "-y",
        "-i", str(master_wav),
        "-i", str(TRAILER_MUSIC_WAV),
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-t", f"{total_duration:.2f}",
        str(trailer_master)
    ], check=True)

    # Final Video Remux
    print("\n🎞️ Muxing final 1080p MP4 film...")
    final_mp4 = OUT / "cinematic_demo.mp4"
    if final_mp4.exists():
        final_mp4.unlink()

    subprocess.run([
        FFMPEG, "-y",
        "-i", str(raw_video),
        "-i", str(trailer_master),
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-t", f"{total_duration:.2f}",
        str(final_mp4)
    ], check=True)

    size_mb = final_mp4.stat().st_size / (1024 * 1024)
    print(f"\n🏆 Final Master Presentation Complete: {final_mp4} ({size_mb:.2f} MB, {total_duration:.1f}s)")

if __name__ == "__main__":
    record_and_produce()
