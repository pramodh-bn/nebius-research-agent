"""Cinematic Video Production Script for Research Courtroom (Team All Vibes).

Captures:
1. Authentic 1080p Playwright recording of React UI (http://localhost:3000).
2. Scene-by-scene narrated voiceover using Windows Speech Synthesis.
3. Original procedural cinematic ambient musical bed (sub-bass pulses, atmospheric pads).
4. Synchronized SRT subtitles.
5. High-quality H.264 MP4 export via FFmpeg.
"""
import math
import os
import struct
import subprocess
import time
import wave
from pathlib import Path
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

OUT = Path("demo_out")
OUT.mkdir(exist_ok=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
URL = "http://localhost:3000"
QUESTION = "Does intermittent fasting improve long-term weight loss compared with calorie restriction?"
CHALLENGE = "Is there newer clinical evidence from randomized trials longer than 12 months?"
BLOCKED_URL = "http://169.254.169.254/latest/meta-data/"

# 3-Minute Cinematic Narration (approx 340 words, measured pacing, authoritative tone)
SCENES = [
    {
        "id": "act1_hook",
        "title": "Act I - The Consensus Illusion",
        "text": "Ask standard AI a contested scientific question, and it gives you a smooth, polite answer. But real research doesn't have a single consensus. It has opposing data, conflicting clinical trials, and sharp debate. When AI flattens that tension into a one-sided summary, it hides the truth.",
    },
    {
        "id": "act2_title",
        "title": "Act II - The Invention",
        "text": "All Vibes presents Research Courtroom. Created and engineered by Pramodh Nanjayya for the Nebius Hackathon. We replace polite summarization with an adversarial trial: a Prosecution, a Defense, and an impartial Judge.",
    },
    {
        "id": "act2_stream",
        "title": "Act II - Live Deliberation Stream",
        "text": "I file a real contested question: does intermittent fasting improve long-term weight loss compared with calorie restriction? Watch the live deliberation feed. Tavily searches real-time sources, hashes each excerpt, and seals the evidence ledger.",
    },
    {
        "id": "act2_arguments",
        "title": "Act II - Opposing Counsel & Verification",
        "text": "The document drafts live. The Prosecution argues the affirmative case from admitted evidence. The Defense counters with trial duration limits and protocol heterogeneity. Every claim is audited by a separate Nebius Qwen reasoner call that verifies whether the excerpt actually supports the claim.",
    },
    {
        "id": "act2_cross_exam",
        "title": "Act II - Cross-Examination",
        "text": "Counsel then cross-examine each other directly on evidence veracity. Notice the citations: hallucinated source IDs are stripped instantly. If evidence cannot be verified, the court is forced by code to rule inconclusive.",
    },
    {
        "id": "act2_verdict_popup",
        "title": "Act II - The Verdict Pop-Up",
        "text": "The verdict is reached. An instant ruling announcement confirms the finding: inconclusive for long-term superiority, with comparable 12-month outcomes. We review the full judicial reasoning, findings matrix, and unresolved questions.",
    },
    {
        "id": "act3_reconsideration",
        "title": "Act III - Interactive Challenge & SSRF Defense",
        "text": "Now, we cross-examine the court. When I challenge with a blocked cloud metadata address, hardened SSRF protections refuse the socket cold. And when I introduce genuine evidence, the court tracks revisions without flipping arbitrarily.",
    },
    {
        "id": "act3_conclusion",
        "title": "Act III - The Future is Already Running",
        "text": "Fifty-six automated tests. Full-stack SSE streaming. Zero fabricated citations. Research Courtroom proves that the future of AI research isn't about confident summaries. It is about verifiable truth.",
    },
]


def generate_tts(scene_id: str, text: str) -> tuple[Path, float]:
    """Generate clean narration WAV file using Windows Speech Synthesis."""
    wav_path = OUT / f"{scene_id}.wav"
    # Pacing: rate = -1 for deliberate documentary pacing
    ps_cmd = (
        "Add-Type -AssemblyName System.Speech; "
        "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$synth.Rate = -1; "
        "$synth.Volume = 100; "
        f"$synth.SetOutputToWaveFile('{wav_path.resolve()}'); "
        f"$synth.Speak(@'\n{text}\n'@); "
        "$synth.Dispose()"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
    with wave.open(str(wav_path), "rb") as w:
        duration = w.getnframes() / w.getframerate()
    return wav_path, duration


def generate_cinematic_music(total_seconds: float) -> Path:
    """Generate an original procedural ambient cinematic soundscape (sub-bass pulse, warm drones)."""
    music_wav = OUT / "cinematic_soundtrack.wav"
    sample_rate = 44100
    total_frames = int(sample_rate * total_seconds)

    # Frequencies: D minor root (D2: 73.42 Hz, A2: 110 Hz, F2: 87.31 Hz, D3: 146.83 Hz)
    f_root = 73.42
    f_fifth = 110.0
    f_third = 87.31

    with wave.open(str(music_wav), "wb") as w:
        w.setnchannels(2)  # Stereo
        w.setsampwidth(2)  # 16-bit
        w.setframerate(sample_rate)

        buf = bytearray()
        for i in range(total_frames):
            t = i / sample_rate
            # 1. Slow, deep sub-bass pulse (0.4 Hz breathing)
            pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 0.35 * t)
            sub = math.sin(2 * math.pi * f_root * t) * 0.18 * pulse

            # 2. Warm ambient drone pad
            pad_1 = math.sin(2 * math.pi * f_fifth * t) * 0.08
            pad_2 = math.sin(2 * math.pi * f_third * t) * 0.06
            pad_3 = math.sin(2 * math.pi * (f_root * 2) * t) * 0.04

            # 3. High harmonic shimmer (evolving slowly)
            shimmer = math.sin(2 * math.pi * 440.0 * t + math.sin(2 * math.pi * 0.1 * t)) * 0.015

            # 4. Subtle rhythmic heartbeat in Act II (starts at t > 35)
            beat = 0.0
            if t > 35:
                beat_phase = (t * 1.5) % 1.0  # 90 BPM
                if beat_phase < 0.15:
                    beat = math.sin(2 * math.pi * 55.0 * (beat_phase / 0.15)) * 0.12 * (1.0 - beat_phase / 0.15)

            # Master mix & fade out at end
            fade = 1.0
            if t > total_seconds - 5.0:
                fade = max(0.0, (total_seconds - t) / 5.0)

            sample_l = int((sub + pad_1 + pad_3 + shimmer + beat) * fade * 32767 * 0.75)
            sample_r = int((sub + pad_2 + pad_3 - shimmer + beat) * fade * 32767 * 0.75)
            sample_l = max(-32767, min(32767, sample_l))
            sample_r = max(-32767, min(32767, sample_r))
            buf.extend(struct.pack("<hh", sample_l, sample_r))

        w.writeframes(buf)
    return music_wav


def generate_srt(scene_timings: list[tuple[float, float, str]], srt_path: Path):
    """Generate synchronized SRT subtitles."""
    def format_ts(seconds: float) -> str:
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

    lines = []
    for idx, (start_t, end_t, text) in enumerate(scene_timings, 1):
        lines.append(str(idx))
        lines.append(f"{format_ts(start_t)} --> {format_ts(end_t)}")
        # Break text into max 2 readable lines
        words = text.split()
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        lines.append(line1)
        if line2:
            lines.append(line2)
        lines.append("")

    srt_path.write_text("\n".join(lines), encoding="utf-8")


def record_cinematic_demo():
    print("=" * 60)
    print("🎬 Starting Cinematic Hackathon Video Production")
    print("=" * 60)

    # Step 1: Synthesize all speech clips
    print("\n🎙️ Generating voiceover narration scenes...")
    scene_clips = {}
    for sc in SCENES:
        p, dur = generate_tts(sc["id"], sc["text"])
        scene_clips[sc["id"]] = (p, dur)
        print(f"  • {sc['title']}: {dur:.1f}s")

    raw_video_dir = OUT / "raw_video"
    raw_video_dir.mkdir(exist_ok=True)

    # Step 2: Screen recording with Playwright at 1920x1080
    print("\n🖥️ Capturing live web application interactions (1920x1080)...")
    narration_cues = []  # (start_time, wav_path)
    scene_timings = []   # (start_time, end_time, text)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(raw_video_dir),
            record_video_size={"width": 1920, "height": 1080},
        )
        page = context.new_page()
        t_start = time.time()
        curr_time = lambda: time.time() - t_start

        def trigger_scene(scene_id: str, pad_after: float = 1.0):
            wav, dur = scene_clips[scene_id]
            st = curr_time()
            narration_cues.append((st, wav))
            text = next(s["text"] for s in SCENES if s["id"] == scene_id)
            scene_timings.append((st, st + dur, text))
            return st + dur + pad_after

        def hold_until(target_t: float):
            remaining = target_t - curr_time()
            if remaining > 0:
                page.wait_for_timeout(int(remaining * 1000))

        # --- Scene 1: Act I Hook (Courtroom Recess) ---
        page.goto(URL)
        page.wait_for_selector(".brand-name", timeout=15000)
        end_t = trigger_scene("act1_hook", pad_after=1.5)
        # Gently pan across the clean ready state
        page.mouse.wheel(0, 200)
        page.wait_for_timeout(800)
        page.mouse.wheel(0, -200)
        hold_until(end_t)

        # --- Scene 2: Act II Title Reveal ---
        end_t = trigger_scene("act2_title", pad_after=1.5)
        page.wait_for_timeout(1000)
        # Select Preset 1
        preset_btn = page.get_by_role("button", name="Intermittent fasting")
        preset_btn.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        preset_btn.click()
        page.wait_for_timeout(800)
        hold_until(end_t)

        # --- Scene 3: Act II Filing & Live Stream ---
        end_t = trigger_scene("act2_stream", pad_after=1.5)
        open_btn = page.get_by_role("button", name="Open trial")
        open_btn.click()
        # Wait for live deliberation stream box to appear
        page.wait_for_selector(".live-stream-box", timeout=15000)
        hold_until(end_t)

        # --- Scene 4: Act II Arguments & Verification ---
        end_t = trigger_scene("act2_arguments", pad_after=1.5)
        # Wait until claims appear
        page.wait_for_selector(".argument.prosecution", timeout=30000)
        page.get_by_text("Opening arguments").first.scroll_into_view_if_needed()
        page.wait_for_timeout(1500)
        # Click a citation to show evidence excerpt in drawer
        citations = page.locator(".citation")
        if citations.count() > 0:
            citations.first.click()
            page.wait_for_timeout(1500)
            page.keyboard.press("Escape")
        hold_until(end_t)

        # --- Scene 5: Act II Cross-Examination ---
        end_t = trigger_scene("act2_cross_exam", pad_after=1.5)
        page.get_by_text("Cross-examination").first.scroll_into_view_if_needed()
        page.wait_for_timeout(2000)
        hold_until(end_t)

        # --- Scene 6: Act II The Verdict Pop-Up ---
        end_t = trigger_scene("act2_verdict_popup", pad_after=2.0)
        # Wait for verdict pop-up dialog to appear
        try:
            page.wait_for_selector("text=The Verdict Has Been Reached", timeout=60000)
            page.wait_for_timeout(2500)
            # Click Review Full Verdict button to smoothly scroll down
            review_btn = page.get_by_role("button", name="Review Full Verdict")
            if review_btn.count() > 0:
                review_btn.click()
                page.wait_for_timeout(2000)
        except Exception:
            page.get_by_text("Judicial verdict").first.scroll_into_view_if_needed()
        hold_until(end_t)

        # --- Scene 7: Act III Interactive Challenge & SSRF Security ---
        end_t = trigger_scene("act3_reconsideration", pad_after=1.5)
        page.get_by_text("Cross-examine the court").first.scroll_into_view_if_needed()
        page.wait_for_timeout(600)
        challenge_input = page.locator("#challenge")
        url_input = page.locator("#source-url")
        if challenge_input.count() > 0 and url_input.count() > 0:
            challenge_input.fill(CHALLENGE)
            url_input.fill(BLOCKED_URL)
            page.wait_for_timeout(800)
            page.get_by_role("button", name="Challenge verdict").click()
            # Wait for red security alert
            page.wait_for_selector(".notice.error", timeout=10000)
            page.wait_for_timeout(2000)
        hold_until(end_t)

        # --- Scene 8: Act III Conclusion ---
        end_t = trigger_scene("act3_conclusion", pad_after=2.5)
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(2000)
        hold_until(end_t)

        total_video_duration = curr_time()
        context.close()
        browser.close()

    # Locate recorded video file
    video_files = list(raw_video_dir.glob("*.webm"))
    if not video_files:
        raise RuntimeError("Playwright did not output a webm recording")
    raw_video = video_files[0]
    print(f"✅ Raw screen capture complete ({total_video_duration:.1f}s): {raw_video}")

    # Step 3: Generate synchronized SRT subtitles
    srt_file = OUT / "research_courtroom.srt"
    generate_srt(scene_timings, srt_file)
    print(f"✅ Subtitles generated: {srt_file}")

    # Step 4: Generate original procedural cinematic soundtrack
    print("\n🎵 Generating original cinematic music bed...")
    music_wav = generate_cinematic_music(total_video_duration + 3.0)
    print(f"✅ Soundtrack generated: {music_wav}")

    # Step 5: Mix speech clips onto master narration track
    print("\n🎛️ Assembling voiceover audio track...")
    voice_track = OUT / "voiceover_master.wav"
    # Detect native sample rate from speech synthesis clips (22050 Hz on Windows TTS)
    first_clip = next(iter(scene_clips.values()))[0]
    with wave.open(str(first_clip), "rb") as w:
        sample_rate = w.getframerate()
    print(f"  • Voice sample rate detected: {sample_rate} Hz")

    total_samples = int(sample_rate * (total_video_duration + 2.0))
    master_samples = [0] * total_samples

    for start_t, wav_p in narration_cues:
        with wave.open(str(wav_p), "rb") as w:
            n_frames = w.getnframes()
            ch = w.getnchannels()
            sw = w.getsampwidth()
            fr = w.getframerate()
            raw = w.readframes(n_frames)

            start_idx = int(start_t * sample_rate)
            if sw == 2:
                fmt = f"<{n_frames * ch}h"
                samples = struct.unpack(fmt, raw)
                step = ch
                for j in range(0, len(samples), step):
                    target_idx = start_idx + (j // step)
                    if target_idx < total_samples:
                        master_samples[target_idx] += samples[j]

    # Normalize voice track
    max_val = max(abs(s) for s in master_samples) or 1
    gain = 28000 / max_val if max_val > 0 else 1.0
    with wave.open(str(voice_track), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        packed = struct.pack(f"<{len(master_samples)}h", *[max(-32767, min(32767, int(s * gain))) for s in master_samples])
        w.writeframes(packed)
    print(f"✅ Master voice track compiled: {voice_track}")

    # Step 6: Final Mux with FFmpeg (Audio ducking + 1080p H.264 encode)
    print("\n🎞️ Muxing cinematic film with FFmpeg...")
    final_output = OUT / "cinematic_demo.mp4"
    if final_output.exists():
        final_output.unlink()

    # FFmpeg filter: voice loud and clear (volume=1.2), music subtly ambient (volume=0.07)
    filter_complex = (
        "[1:a]volume=1.2[voice];"
        "[2:a]volume=0.07[music];"
        "[voice][music]amix=inputs=2:duration=first:dropout_transition=2[aout];"
        "[0:v]fps=30,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[vout]"
    )

    cmd = [
        FFMPEG,
        "-y",
        "-i", str(raw_video),
        "-i", str(voice_track),
        "-i", str(music_wav),
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", f"{total_video_duration:.2f}",
        str(final_output),
    ]

    subprocess.run(cmd, check=True)
    size_mb = final_output.stat().st_size / (1024 * 1024)
    print(f"\n🏆 Final Cinematic Presentation Complete: {final_output} ({size_mb:.2f} MB, {total_video_duration:.1f}s)")


if __name__ == "__main__":
    record_cinematic_demo()
