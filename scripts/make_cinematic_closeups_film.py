"""Master Presentation Film Producer: 8 Gamma Keynote Slides + Live Courtroom Demo with Camera Close-ups.

Features:
- Part 1: Gamma Keynote Slides (Slides 1 to 6)
    * Slide 1: Welcome & Attribution (neural narration + user voice splice "Pramodh Nanjayya")
    * Slide 2: The Crisis of Polite Consensus (The Cost of False Certainty)
    * Slide 3: The Paradigm Shift (Don't search the science — put it on trial)
    * Slide 4: Tripartite Jurisprudence (Autonomous roles on Nebius Qwen reasoner)
    * Slide 5: Defensive Invariants (56 tests, 0 hallucinated citations, SSRF firewall)
    * Slide 6: The Live Courtroom Experience (Real-time deliberation & auditability)
- Part 2: Active Live Demo with Dynamic Camera Close-ups & Glassmorphism HUD Badges
    * Focus 1: Zoom to filing input with real-time human typing
    * Focus 2: Zoom to real-time SSE deliberation stream
    * Focus 3: Zoom to Prosecution vs. Defense & Click citation provenance drawer
    * Focus 4: Zoom to Instant Verdict Pop-Up Announcement Modal (PERFECTLY SYNCED)
    * Focus 5: Zoom to Cross-examination SSRF security block on 169.254.169.254
- Part 3: Empirical Validation & Grand Finale (Slides 7 and 8)
    * Slide 7: Validation across clinical trials (Refusal to manufacture consensus)
    * Slide 8: Grand Finale Closing Card & GitHub CTA ("Find it on GitHub and run Research Courtroom today")
- Soundtrack: Hollywood trailer score ('The Epic 2' by Rafael Krux) with Continuous Looping + Dynamic Sidechain Ducking
- Runtime: ~2m 50s - 3m 05s
"""
import asyncio
import os
from pathlib import Path
import struct
import subprocess
import sys
import time
import urllib.request
import wave
import edge_tts
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "demo_out"
OUT.mkdir(exist_ok=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
VOICE = "en-US-ChristopherNeural"
SAMPLE_RATE = 24000

APP_URL = "http://localhost:3000"
SLIDES_HTML = (OUT / "gamma_slides_player.html").resolve().as_uri()
QUESTION = "Does intermittent fasting improve long-term weight loss compared with calorie restriction?"
CHALLENGE = "Is there newer clinical evidence from randomized trials longer than 12 months?"
BLOCKED_URL = "http://169.254.169.254/latest/meta-data/"
USER_VOICE_WAV = OUT / "user_voice.wav"
TRAILER_MUSIC_WAV = OUT / "the_epic_2.wav"

SCENES = [
    # --- PART 1: GAMMA KEYNOTE SLIDES 1 to 6 (~65s) ---
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
        "text": "Why does this exist? When you ask standard AI a clinical research question, it gives you a polite, false agreement. Study A used forty patients for eight weeks and claimed success. Study B used five hundred patients for eighteen months and showed the opposite. Standard chatbots blur them together into dangerous false certainty. In medicine and science, that false certainty costs lives.",
    },
    {
        "id": "s3_shift",
        "type": "neural",
        "text": "Instead of treating deep research like an open-ended search query, Research Courtroom structures inquiry into an adversarial trial. We don't search the science—we put it on trial.",
    },
    {
        "id": "s4_arch",
        "type": "neural",
        "text": "Three autonomous roles, powered by Nebius Qwen reasoner. A Prosecution argues the affirmative case. A Defense dismantles study methodology and exposes limits. And an independent auditor verifies every excerpt before the Judge rules.",
    },
    {
        "id": "s5_invariants",
        "type": "neural",
        "text": "Strict defensive invariants: zero hallucinated citations, real-time SSRF defense blocking cloud metadata theft cold, and fifty-six automated tests ensuring system guarantees hold.",
    },
    {
        "id": "s6_preview",
        "type": "neural",
        "text": "The trial plays out live with full provenance. Let us step into the live courtroom.",
    },

    # --- PART 2: ACTIVE LIVE DEMO WITH CAMERA CLOSE-UPS (~80s) ---
    {
        "id": "d1_stream",
        "type": "neural",
        "text": "We file a contested clinical case. Watch the live deliberation stream. Tavily searches real-time sources, hashes each excerpt, and counsel drafts live into the document.",
    },
    {
        "id": "d2_audit",
        "type": "neural",
        "text": "Every citation binds directly to a verified excerpt. If citations are hallucinated, they are stripped immediately. Counsel cross-examine each other on veracity.",
    },
    {
        "id": "d3_verdict",
        "type": "neural",
        "text": "The verdict has been reached. An instant ruling announcement confirms the finding: inconclusive for long-term superiority. The court refuses to manufacture consensus.",
    },
    {
        "id": "d4_challenge",
        "type": "neural",
        "text": "Finally, we cross-examine the court with a blocked cloud metadata address. Hardened security refuses the socket cold. Fifty-six tests passing.",
    },

    # --- PART 3: EMPIRICAL VALIDATION & GRAND FINALE SLIDES 7 & 8 (~25s) ---
    {
        "id": "c1_results",
        "type": "neural",
        "text": "Across contested trials, the courtroom refused to manufacture compromise. When clinical evidence showed equal weight loss at twelve months, the court ruled Inconclusive, backed by verified evidence receipts.",
    },
    {
        "id": "c2_finale",
        "type": "neural",
        "text": "Truth is not a compromise. Don't search for consensus—put the science on trial. Find it on GitHub and run Research Courtroom today.",
    },
]

async def generate_speech_clip(text: str, out_wav: Path, rate: str = "+3%"):
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
    print("\n🎙️ Loading/Generating narration clips (Neural AI + User Voice)...")
    clips = {}
    for sc in SCENES:
        sid = sc["id"]
        out_p = OUT / f"{sid}_clip.wav"
        if not out_p.exists() or out_p.stat().st_size < 1000:
            if sc.get("type") == "neural":
                await generate_speech_clip(sc["text"], out_p, rate="+3%")
                normalize_wav(out_p, out_p)
            elif sc.get("type") == "composite_user":
                p_a = OUT / f"{sid}_pa.wav"
                p_c = OUT / f"{sid}_pc.wav"
                p_u = OUT / f"{sid}_u.wav"
                await generate_speech_clip(sc["part_a"], p_a, rate="+1%")
                await generate_speech_clip(sc["part_c"], p_c, rate="+2%")
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
        # PHASE 1: GAMMA KEYNOTE SLIDES 1 to 6 (~65s)
        # =====================================================================
        page.goto(SLIDES_HTML)
        page.wait_for_selector("#slide-1", timeout=10000)
        page.wait_for_timeout(400)

        # Slide 1: Title & Attribution (with user's own voice)
        end_t = trigger_cue("s1_title", pad=0.6)
        wait_until(end_t)

        # Slide 2: The Crisis of Polite Consensus
        page.evaluate("window.goToSlide(2)")
        end_t = trigger_cue("s2_problem", pad=0.6)
        wait_until(end_t)

        # Slide 3: The Paradigm Shift
        page.evaluate("window.goToSlide(3)")
        end_t = trigger_cue("s3_shift", pad=0.6)
        wait_until(end_t)

        # Slide 4: Tripartite Jurisprudence on Nebius
        page.evaluate("window.goToSlide(4)")
        end_t = trigger_cue("s4_arch", pad=0.6)
        wait_until(end_t)

        # Slide 5: Defensive Invariants (56 Tests, SSRF, Zero Hallucinations)
        page.evaluate("window.goToSlide(5)")
        end_t = trigger_cue("s5_invariants", pad=0.6)
        wait_until(end_t)

        # Slide 6: The Trial Plays Out Live
        page.evaluate("window.goToSlide(6)")
        end_t = trigger_cue("s6_preview", pad=0.8)
        wait_until(end_t)

        # =====================================================================
        # PHASE 2: ACTIVE LIVE APP DEMO WITH CLOSE-UPS (~80s)
        # =====================================================================
        page.goto(APP_URL)
        page.wait_for_selector(".brand-name", timeout=25000)
        page.wait_for_timeout(500)
        page.evaluate(CAMERA_CONTROLLER_JS)

        # Close-up 1: Zoom to search bar & live typing
        page.evaluate("window.zoomTo('.filing-form', 1.5, '🔍 Research Question · Live Input')")
        page.wait_for_timeout(500)

        input_box = page.locator("input[aria-label='Research question']")
        input_box.focus()
        input_box.press_sequentially(QUESTION, delay=8)
        input_box.fill(QUESTION)
        page.wait_for_timeout(300)

        # Click Open Trial button
        submit_btn = page.locator("button[type='submit']")
        submit_btn.click()
        page.wait_for_timeout(400)

        # Preset fallback check to guarantee trial opening
        if page.locator(".live-stream-box").count() == 0:
            preset_btn = page.get_by_role("button", name="Intermittent fasting")
            if preset_btn.count() > 0:
                preset_btn.click()
                page.wait_for_timeout(200)
                page.locator("button[type='submit']").click()

        # Close-up 2: Zoom to live stream deliberation ticker
        try:
            page.wait_for_selector(".live-stream-box", timeout=15000)
            page.evaluate("window.zoomTo('.live-stream-box', 1.4, '⚡ Real-Time SSE Deliberation Stream')")
        except Exception:
            pass
        end_t = trigger_cue("d1_stream", pad=0.8)
        wait_until(end_t)

        # Close-up 3: Zoom to Opening Arguments & Citation Provenance
        try:
            page.wait_for_selector(".argument.prosecution", timeout=30000)
            page.evaluate("window.zoomTo('.arguments', 1.3, '🏛️ Opposing Counsel · Prosecution vs. Defense')")
            page.wait_for_timeout(1000)
        except Exception:
            pass
        end_t = trigger_cue("d2_audit", pad=0.8)
        page.wait_for_timeout(1200)

        # Click verified citation to open excerpt drawer
        citations = page.locator(".citation")
        if citations.count() > 0:
            citations.first.click()
            page.evaluate("window.showHud('📖 Provenance Ledger · Excerpt Audit')")
            page.wait_for_timeout(2200)
            page.keyboard.press("Escape")
        wait_until(end_t)

        # Close-up 4: Instant Verdict Announcement Modal Dialog (PERFECT SYNC: Wait for modal FIRST!)
        try:
            page.wait_for_selector("text=The Verdict Has Been Reached", timeout=60000)
            page.evaluate("window.resetZoom('⚖️ Judicial Verdict · Inconclusive Invariant')")
            page.wait_for_timeout(600)
        except Exception:
            page.get_by_text("Judicial verdict").first.scroll_into_view_if_needed()

        # Now that the modal is physically on screen, trigger the narration cue!
        end_t = trigger_cue("d3_verdict", pad=1.0)
        page.wait_for_timeout(2500)
        review_btn = page.get_by_role("button", name="Review Full Verdict")
        if review_btn.count() > 0:
            review_btn.click()
            page.wait_for_timeout(1500)
        wait_until(end_t)

        # Close-up 5: Cross-Examination & SSRF Security Block
        page.get_by_text("Cross-examine the court").first.scroll_into_view_if_needed()
        page.evaluate("window.zoomTo('.challenge-form', 1.45, '🛡️ Hardened SSRF Defense · Metadata Block')")
        page.wait_for_timeout(400)
        end_t = trigger_cue("d4_challenge", pad=0.8)
        challenge_input = page.locator("#challenge")
        url_input = page.locator("#source-url")
        if challenge_input.count() > 0 and url_input.count() > 0:
            challenge_input.fill(CHALLENGE)
            url_input.fill(BLOCKED_URL)
            page.wait_for_timeout(500)
            page.get_by_role("button", name="Challenge verdict").click()
            try:
                page.wait_for_selector(".notice.error", timeout=10000)
                page.wait_for_timeout(2000)
            except Exception:
                pass
        wait_until(end_t)

        # =====================================================================
        # PHASE 3: EMPIRICAL VALIDATION & GRAND FINALE SLIDES 7 & 8 (~25s)
        # =====================================================================
        page.goto(SLIDES_HTML)
        page.wait_for_selector("#slide-7", timeout=10000)
        page.evaluate("window.goToSlide(7)")
        end_t = trigger_cue("c1_results", pad=0.6)
        wait_until(end_t)

        # Slide 8: Grand Finale Closing Card & GitHub CTA
        page.evaluate("window.goToSlide(8)")
        end_t = trigger_cue("c2_finale", pad=3.5)
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

    # Mix with Trailer Music using Continuous Looping and Sidechain Ducking
    print("\n🎵 Mastering Hollywood Trailer Soundtrack with Continuous Looping & Sidechain Ducking...")
    trailer_master = OUT / "slides_soundtrack_master.wav"
    fade_st = max(0, total_duration - 2.5)
    filter_complex = (
        f"[1:a]afade=t=out:st={fade_st:.1f}:d=2.4,volume=0.32[music];"
        f"[music][0:a]sidechaincompress=threshold=0.035:ratio=4:attack=40:release=400[ducked];"
        f"[0:a]volume=1.3[voice];"
        f"[voice][ducked]amix=inputs=2:duration=first:dropout_transition=2[aout]"
    )
    subprocess.run([
        FFMPEG, "-y",
        "-i", str(master_wav),
        "-stream_loop", "-1",
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
