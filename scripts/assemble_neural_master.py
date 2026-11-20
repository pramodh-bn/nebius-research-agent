import math
import struct
import subprocess
import wave
from pathlib import Path
import imageio_ffmpeg

OUT = Path("demo_out")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SAMPLE_RATE = 24000
TOTAL_DURATION = 167.6

CUES = [
    (3.50, OUT / "act1_hook_neural.wav"),
    (27.50, OUT / "act2_title_neural.wav"),
    (48.50, OUT / "act2_stream_neural.wav"),
    (67.50, OUT / "act2_arguments_neural.wav"),
    (89.00, OUT / "act2_cross_exam_neural.wav"),
    (106.50, OUT / "act2_verdict_popup_neural.wav"),
    (126.00, OUT / "act3_reconsideration_neural.wav"),
    (145.50, OUT / "act3_conclusion_neural.wav"),
]

def build_master_track():
    print("🎛️ Assembling 24,000 Hz Studio Neural Voiceover Master Track...")
    total_samples = int(SAMPLE_RATE * (TOTAL_DURATION + 2.0))
    master = [0] * total_samples

    for start_t, wav_p in CUES:
        with wave.open(str(wav_p), "rb") as w:
            n = w.getnframes()
            ch = w.getnchannels()
            sw = w.getsampwidth()
            fr = w.getframerate()
            raw = w.readframes(n)
            
            samples = struct.unpack(f"<{n * ch}h", raw)
            start_idx = int(start_t * SAMPLE_RATE)
            for j in range(0, len(samples), ch):
                idx = start_idx + (j // ch)
                if idx < total_samples:
                    master[idx] += samples[j]
            dur = n / fr
            print(f"  • Placed {wav_p.name} at {start_t:.1f}s (dur: {dur:.1f}s)")

    # Peak normalization
    max_val = max(abs(s) for s in master) or 1
    gain = 28000 / max_val
    print(f"  • Max peak: {max_val}, applying gain: {gain:.2f}")

    master_wav = OUT / "voiceover_neural_master.wav"
    with wave.open(str(master_wav), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        packed = struct.pack(f"<{len(master)}h", *[max(-32767, min(32767, int(s * gain))) for s in master])
        w.writeframes(packed)

    print(f"✅ Neural voiceover master generated: {master_wav} ({TOTAL_DURATION:.1f}s)")
    return master_wav

if __name__ == "__main__":
    build_master_track()
