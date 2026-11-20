"""Master Presentation Film Producer: Close-ups, Camera Motion, and Heroic Closing Card.

Features:
- Part 1: Visual Keynote Slides (Title with user voice, The Purpose/Why, Architecture, Invariants)
- Part 2: Active Live Demo with Dynamic Camera Close-ups & HUD Labels
    * Focus 1: Zoom to search bar during live typing
    * Focus 2: Zoom to live stream deliberation ticker
    * Focus 3: Zoom & highlight Opening Arguments (Prosecution vs. Defense)
    * Focus 4: Zoom to Citation Provenance Drawer
    * Focus 5: Zoom to Instant Verdict Pop-Up Announcement Modal
    * Focus 6: Zoom to Cross-examination SSRF security block
- Part 3: Grand Finale Closing Card (Slide 6)
    * Glowing Scale of Justice emblem
    * Punchline: "Truth is not a compromise. Put the science on trial."
    * Call-To-Action: github.com/pramodh-bn/nebius-research-agent
    * Created & Engineered by Pramodh Nanjayya · Team All Vibes
- Soundtrack: Hollywood trailer score ('The Epic 2' by Rafael Krux) + Sidechain Ducking
- Total Runtime: ~2m 55s (Sub-3 Minutes)
"""
import asyncio
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
QUESTION = "Does intermittent fasting improve long-term weight loss compared with calorie restriction?"
CHALLENGE = "Is there newer clinical evidence from randomized trials longer than 12 months?"
BLOCKED_URL = "http://169.254.169.254/latest/meta-data/"
USER_VOICE_WAV = OUT / "user_voice.wav"
TRAILER_MUSIC_WAV = OUT / "the_epic_2.wav"

SCENES = [
    # --- PART 1: SLIDES (~60s) ---
    {
        "id": "s1_title",
        "type": "composite_user",
        "part_a": "All Vibes presents: Research Courtroom. Created and engineered by...",
        "user_wav": str(USER_VOICE_WAV),
        "part_c": "...for the Nebius Hackathon. We put contested science on trial.",
    },
    {
        "id": "s2_problem",
        "type": "neural",
        "text": "Why does this exist? When you ask an AI about clinical research, it gives you a polite, false agreement. Study A used forty patients for eight weeks and claimed success. Study B used five hundred patients for eighteen months and showed the opposite. Standard AI blurs them together into dangerous false certainty. Research Courtroom dismantles that illusion.",
    },
    {
        "id": "s3_arch",
        "type": "neural",
        "text": "Its purpose is simple: don't treat scientific research like a search query—treat it like a trial. A Prosecution and Defense battle over evidence, audited by an independent Nebius Qwen reasoner before the Judge rules.",
    },
    {
        "id": "s4_security",
        "type": "neural",
        "text": "Zero hallucinated citations. Hardened against cloud metadata theft. And the courage to rule inconclusive when evidence fails to prove the case. Fifty-six automated tests.",
    },
    {
        "id": "s5_demo_intro",
        "type": "neural",
        "text": "And now, let us step into the live courtroom.",
    },
    # --- PART 2: LIVE DEMO WITH CAMERA CLOSE-UPS (~85s) ---
    {
        "id": "d1_stream",
        "type": "neural",
        "text": "We file a contested clinical case. Watch the live deliberation stream. Tavily searches real-time sources, hashes each excerpt, and counsel drafts live into the document.",
    },
    {
        "id": "d2_audit",
        "type": "neural",
        "text": "Every citation binds directly to a verified excerpt. If citations are hallucinated, they are stripped immediately. Counsel then cross-examine each other directly on veracity.",
    },
    {
        "id": "d3_verdict",
        "type": "neural",
        "text": "The verdict has been reached. An instant ruling announcement confirms the finding: inconclusive for long-term superiority. We review the full judicial reasoning.",
    },
    {
        "id": "d4_challenge",
        "type": "neural",
        "text": "Finally, we cross-examine the court with a blocked cloud metadata address. Hardened security refuses the socket cold. Fifty-six tests passing.",
    },
    # --- PART 3: HEROIC CLOSING CARD (~25s) ---
    {
        "id": "c1_closing",
        "type": "neural",
        "text": "Truth is not a compromise. Don't search for consensus—put the science on trial. Explore the codebase and run Research Courtroom today at github.com/pramodh-bn/nebius-research-agent.",
    },
]

async def generate_speech_clip(text: str, out_wav: Path, rate: str = "+2%"):
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
            await generate_speech_clip(sc["text"], out_p, rate="+2%")
            normalize_wav(out_p, out_p)
        elif sc.get("type") == "composite_user":
            p_a = OUT / f"{sid}_pa.wav"
            p_c = OUT / f"{sid}_pc.wav"
            p_u = OUT / f"{sid}_u.wav"
            await generate_speech_clip(sc["part_a"], p_a, rate="+1%")
            await generate_speech_clip(sc["part_c"], p_c, rate="+1%")
            subprocess.run(["ffmpeg", "-y", "-i", sc["user_wav"], "-ar", str(SAMPLE_RATE), "-ac", "1", str(p_u)], check=True, capture_output=True)
            normalize_wav(p_u, p_u)
            
            silence_samples = int(SAMPLE_RATE * 0.25)
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

CAMERA_CONTROLLER_JS = """
(() => {
    if (document.getElementById('demo-hud-label')) return;
    const hud = document.createElement('div');
    hud.id = 'demo-hud-label';
    hud.style.position = 'fixed';
    hud.style.left = '60px';
    hud.style.bottom = '80px';
    hud.style.padding = '14px 26px';
    hud.style.borderRadius = '14px';
    hud.style.fontFamily = 'Plus Jakarta Sans, -apple-system, sans-serif';
    hud.style.fontWeight = '700';
    hud.style.fontSize = '26px';
    hud.style.color = '#ffffff';
    hud.style.background = 'rgba(15, 23, 42, 0.94)';
    hud.style.border = '2px solid #60a5fa';
    hud.style.boxShadow = '0 20px 50px rgba(0,0,0,0.65), 0 0 30px rgba(96,165,250,0.35)';
    hud.style.backdropFilter = 'blur(16px)';
    hud.style.opacity = '0';
    hud.style.transform = 'translateY(20px)';
    hud.style.transition = 'all 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
    hud.style.zIndex = '999999';
    hud.style.pointerEvents = 'none';
    document.body.appendChild(hud);

    window.showHud = (text) => {
        hud.innerText = text;
        hud.style.opacity = '1';
        hud.style.transform = 'translateY(0)';
    };

    window.hideHud = () => {
        hud.style.opacity = '0';
        hud.style.transform = 'translateY(20px)';
    };

    const root = document.querySelector('main') || document.querySelector('#root') || document.body;
    root.style.transformOrigin = '0 0';
    root.style.transition = 'transform 0.85s cubic-bezier(0.16, 1, 0.3, 1)';

    window.zoomTo = (selector, scale = 1.45, label = null) => {
        const el = document.querySelector(selector);
        if (!el) return;
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        setTimeout(() => {
            const rect = el.getBoundingClientRect();
            const cx = rect.left + rect.width / 2;
            const cy = rect.top + rect.height / 2;
            const tx = Math.min(0, Math.max(1920 - 1920 * scale, 960 - cx * scale));
            const ty = Math.min(0, Math.max(1080 - 1080 * scale, 540 - cy * scale));
            root.style.transform = `translate(${tx}px, ${ty}px) scale(${scale})`;
            if (label) window.showHud(label);
        }, 200);
    };

    window.resetZoom = (label = null) => {
        root.style.transform = 'none';
        if (label) window.showHud(label);
        else window.hideHud();
    };
})();
"""

def record_and_produce():
    clips = asyncio.run(prepare_all_audio())

    raw_dir = OUT / "slides_raw_video"
    raw_dir.mkdir(exist_ok=True)
    for f in raw_dir.glob("*.webm"):
        f.unlink()

    print("\n🖥️ Capturing 1080p Presentation with Dynamic Camera & Closing Card...")
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

        def trigger_cue(sid: str, pad: float = 0.5):
            wav_p, dur = clips[sid]
            st = elapsed()
            narration_cues.append((st, wav_p))
            return st + dur + pad

        def wait_until(target_t: float):
            rem = target_t - elapsed()
            if rem > 0:
                page.wait_for_timeout(int(rem * 1000))

        # =====================================================================
        # PHASE 1: KEYNOTE SLIDES (~60s)
        # =====================================================================
        page.goto(SLIDES_HTML)
        page.wait_for_selector("#slide-1", timeout=10000)
        page.wait_for_timeout(400)

        # Slide 1: Title & Attribution (with Pramodh's own voice)
        end_t = trigger_cue("s1_title", pad=0.8)
        wait_until(end_t)

        # Slide 2: The Purpose / Why (The Cost of False Certainty)
        page.evaluate("window.goToSlide(2)")
        end_t = trigger_cue("s2_problem", pad=0.8)
        wait_until(end_t)

        # Slide 3: Adversarial Architecture
        page.evaluate("window.goToSlide(3)")
        end_t = trigger_cue("s3_arch", pad=0.8)
        wait_until(end_t)

        # Slide 4: Verification & Defensive Invariants
        page.evaluate("window.goToSlide(4)")
        end_t = trigger_cue("s4_security", pad=0.8)
        wait_until(end_t)

        # Slide 5: Transition to Live Courtroom
        page.evaluate("window.goToSlide(5)")
        end_t = trigger_cue("s5_demo_intro", pad=0.8)
        wait_until(end_t)

        # =====================================================================
        # PHASE 2: ACTIVE LIVE APP DEMO WITH CLOSE-UPS (~85s)
        # =====================================================================
        page.goto(APP_URL)
        page.wait_for_selector(".brand-name", timeout=15000)
        page.wait_for_timeout(400)
        page.evaluate(CAMERA_CONTROLLER_JS)

        # Close-up 1: Zoom to search bar & live typing
        page.evaluate("window.zoomTo('.filing-form', 1.5, '🔍 Research Question · Live Input')")
        page.wait_for_timeout(600)

        input_box = page.locator("input[aria-label='Research question']")
        input_box.focus()
        input_box.press_sequentially(QUESTION, delay=12)
        page.wait_for_timeout(300)

        # Click Open Trial button
        page.get_by_role("button", name="Open trial").click()

        # Close-up 2: Zoom to live stream deliberation ticker
        end_t = trigger_cue("d1_stream", pad=0.8)
        page.wait_for_selector(".live-stream-box", timeout=15000)
        page.evaluate("window.zoomTo('.live-stream-box', 1.4, '⚡ Real-Time SSE Deliberation Stream')")
        wait_until(end_t)

        # Close-up 3: Zoom to Opening Arguments & Citation Provenance
        end_t = trigger_cue("d2_audit", pad=0.8)
        page.wait_for_selector(".argument.prosecution", timeout=30000)
        page.evaluate("window.zoomTo('.arguments', 1.3, '🏛️ Opposing Counsel · Prosecution vs. Defense')")
        page.wait_for_timeout(1800)

        # Click verified citation E9/E10 to open excerpt drawer
        citations = page.locator(".citation")
        if citations.count() > 0:
            citations.first.click()
            page.evaluate("window.showHud('📖 Provenance Ledger · Excerpt Audit')")
            page.wait_for_timeout(2000)
            page.keyboard.press("Escape")
        wait_until(end_t)

        # Close-up 4: Instant Verdict Announcement Modal Dialog
        end_t = trigger_cue("d3_verdict", pad=0.8)
        try:
            page.wait_for_selector("text=The Verdict Has Been Reached", timeout=50000)
            page.evaluate("window.resetZoom('⚖️ Judicial Verdict · Inconclusive Invariant')")
            page.wait_for_timeout(2200)
            review_btn = page.get_by_role("button", name="Review Full Verdict")
            if review_btn.count() > 0:
                review_btn.click()
                page.wait_for_timeout(1000)
        except Exception:
            page.get_by_text("Judicial verdict").first.scroll_into_view_if_needed()
        wait_until(end_t)

        # Close-up 5: Cross-Examination & SSRF Security Block
        end_t = trigger_cue("d4_challenge", pad=0.8)
        page.get_by_text("Cross-examine the court").first.scroll_into_view_if_needed()
        page.evaluate("window.zoomTo('.challenge-form', 1.45, '🛡️ Hardened SSRF Defense · Metadata Block')")
        page.wait_for_timeout(400)
        challenge_input = page.locator("#challenge")
        url_input = page.locator("#source-url")
        if challenge_input.count() > 0 and url_input.count() > 0:
            challenge_input.fill(CHALLENGE)
            url_input.fill(BLOCKED_URL)
            page.wait_for_timeout(500)
            page.get_by_role("button", name="Challenge verdict").click()
            page.wait_for_selector(".notice.error", timeout=10000)
            page.wait_for_timeout(2000)
        wait_until(end_t)

        # =====================================================================
        # PHASE 3: HEROIC CLOSING CARD & GITHUB CTA (~25s)
        # =====================================================================
        # Seamlessly navigate back to Slide 6 (The Closing Card)
        page.goto(SLIDES_HTML)
        page.wait_for_selector("#slide-6", timeout=10000)
        page.evaluate("window.goToSlide(6)")
        page.wait_for_timeout(400)

        end_t = trigger_cue("c1_closing", pad=2.5)
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
    fade_st = max(0, total_duration - 3.5)
    filter_complex = (
        f"[1:a]afade=t=out:st={fade_st:.1f}:d=3.2,volume=0.28[music];"
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
