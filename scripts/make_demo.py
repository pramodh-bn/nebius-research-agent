"""Record the Research Courtroom demo: Playwright screen capture + Windows TTS narration + ffmpeg mux.

Dev-only tooling (pip install playwright imageio-ffmpeg; python -m playwright install chromium).
Requires the app running at http://localhost:8501 with valid keys in .env. Output: demo_out/demo.mp4
Usage: python scripts/make_demo.py
"""
import subprocess, time, wave, os, sys
from pathlib import Path
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

OUT = Path('demo_out'); OUT.mkdir(exist_ok=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
URL = 'http://localhost:8501'
QUESTION = 'Does intermittent fasting improve long-term weight loss compared with calorie restriction?'
CHALLENGE = 'Is there newer evidence from trials longer than 12 months?'

NARRATION = {
    'intro': "This is Research Courtroom, our entry for the Nebius hackathon. For a contested research question, a prosecution and a defense argue from cited web evidence, and an impartial judge rules on the evidence itself, not on the arguments. Inference runs on Nebius Token Factory, and live search runs on Tavily.",
    'file': "I file a real contested question: does intermittent fasting improve long term weight loss compared with calorie restriction. The app searches the web, builds an evidence ledger, then runs the prosecution, the defense, one cross examination, and the judge, with a verification pass after each step.",
    'args': "Here are the opening arguments. Every claim cites ledger sources, shown as clickable links. Each claim also carries a badge from a separate verifier that checks whether the cited excerpt really supports the claim. That label is a model opinion, not proof, and the interface says so.",
    'ledger': "The evidence ledger records, for every source, its link, title, the exact excerpt, the query that found it, and the retrieval time. Duplicates are removed, and unknown citation I Ds are stripped before anything is shown.",
    'verdict': "The cross examination and the judge's verdict come next. The judge cites only ledger evidence, keeps contested findings marked as contested, and lists what remains unresolved. If nothing could be verified, the verdict is forced to read inconclusive.",
    'challenge': "Now I challenge the court with a follow up question about newer evidence. The system retrieves more sources, verifies them, and re judges, while keeping the old verdict.",
    'revision': "The revision history shows the verdict before and after, the new sources added, and the reason. Here the new sources did not change the verdict, and the app says so. It never flips a verdict just because the user pushes.",
    'blocked': "Finally, the failure case. I submit a private network address as a source. The safety checks refuse to fetch it, and it is not forwarded to search either. A public page would be fetched with size and time limits, and still verified like any other source.",
    'outro': "That is Research Courtroom: evidence first, verification on every claim, and verdicts that change only when the evidence does. The repository includes a mocked test suite, an opt in live test, and full documentation. Thank you.",
}


def tts(name, text):
    wav = OUT / f'{name}.wav'
    ps = ("Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
          f"$s.SetOutputToWaveFile('{wav.resolve()}'); $s.Speak(@'\n{text}\n'@); $s.Dispose()")
    subprocess.run(['powershell', '-NoProfile', '-Command', ps], check=True)
    with wave.open(str(wav)) as w:
        return wav, w.getnframes() / w.getframerate()


def main():
    clips = {k: tts(k, v) for k, v in NARRATION.items()}
    for k, (_, d) in clips.items():
        print(f'{k}: {d:.1f}s')
    marks = []  # (start_seconds, wav)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={'width': 1280, 'height': 800},
                                  record_video_dir=str(OUT / 'video'), record_video_size={'width': 1280, 'height': 800})
        page = ctx.new_page()
        t0 = time.time()
        now = lambda: time.time() - t0

        def say(key):
            marks.append((now(), clips[key][0]))
            return now() + clips[key][1] + 0.6  # earliest allowed end of this step

        def hold(until):
            left = until - now()
            if left > 0:
                page.wait_for_timeout(int(left * 1000))

        def show(text, exact=False):
            page.get_by_text(text, exact=exact).first.scroll_into_view_if_needed()
            page.wait_for_timeout(400)

        page.goto(URL); page.get_by_text('File a case').first.wait_for(timeout=60000)
        end = say('intro'); hold(end)

        box = page.get_by_label('File a case')
        box.click(); box.fill(QUESTION); box.press('Enter')
        page.wait_for_timeout(500)
        if page.get_by_text('Judicial verdict').count() == 0:
            page.get_by_role('button', name='Open trial').click()
        end = say('file')
        page.get_by_text('Judicial verdict').first.wait_for(timeout=240000)
        hold(end)

        show('Opening arguments'); end = say('args'); hold(end)
        page.mouse.wheel(0, 500); page.wait_for_timeout(400)
        show('Evidence ledger'); end = say('ledger'); hold(end)
        show('Cross-examination'); page.mouse.wheel(0, 700); end = say('verdict')
        page.wait_for_timeout(3500); show('Judicial verdict'); hold(end)

        show('Cross-examine the court')
        page.get_by_label('Challenge an argument or ask a follow-up').fill(CHALLENGE)
        end = say('challenge')
        page.get_by_role('button', name='Challenge verdict').click()
        page.get_by_text('Verdict revision history').first.wait_for(timeout=240000)
        hold(end)

        show('Verdict revision history'); page.get_by_text('Verdict revision history').first.click()
        page.wait_for_timeout(600); page.mouse.wheel(0, 300)
        end = say('revision'); hold(end)

        show('Cross-examine the court')
        page.get_by_label('Challenge an argument or ask a follow-up').fill('check')
        page.get_by_label('Optional source URL', exact=False).fill('http://169.254.169.254/latest/')
        end = say('blocked')
        page.get_by_role('button', name='Challenge verdict').click()
        page.get_by_text('Submitted URL was blocked').first.wait_for(timeout=240000)
        page.evaluate('window.scrollTo(0, 0)'); hold(end)

        end = say('outro'); hold(end + 1.0)
        total = now()
        vpath = page.video.path()
        ctx.close(); browser.close()

    # build audio track: place each clip at its start offset
    inputs, filters = [], []
    for i, (start, wav) in enumerate(marks):
        inputs += ['-i', str(wav)]
        filters.append(f'[{i}:a]adelay={int(start*1000)}|{int(start*1000)}[a{i}]')
    mix = ''.join(f'[a{i}]' for i in range(len(marks))) + f'amix=inputs={len(marks)}:normalize=0[aout]'
    audio = OUT / 'narration.m4a'
    subprocess.run([FFMPEG, '-y', *inputs, '-filter_complex', ';'.join(filters) + ';' + mix,
                    '-map', '[aout]', '-c:a', 'aac', str(audio)], check=True, capture_output=True)
    final = OUT / 'demo.mp4'
    subprocess.run([FFMPEG, '-y', '-i', str(vpath), '-i', str(audio), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-shortest', str(final)], check=True, capture_output=True)
    print(f'DONE {final} ~{total:.0f}s')


if __name__ == '__main__':
    main()
