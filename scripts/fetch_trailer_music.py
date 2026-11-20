import urllib.request
import re
from pathlib import Path

OUT = Path("demo_out")

def check_track(isrc):
    url = f"https://incompetech.com/music/royalty-free/index.html?isrc={isrc}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        # Find mp3 links
        matches = re.findall(r'href="([^"]+\.mp3)"', html)
        title = re.search(r'<h2>([^<]+)</h2>', html)
        t_name = title.group(1).strip() if title else isrc
        print(f"Track: {t_name}")
        for m in matches:
            print("  Link:", m)
            return m
    return None

if __name__ == "__main__":
    # Exciting Trailer (USUAN1100494), Industrial Cinematic (USUAN1600047), Volatile Reaction (USUAN1400039)
    for isrc in ["USUAN1100494", "USUAN1600047", "USUAN1400039"]:
        try:
            link = check_track(isrc)
            if link:
                dst = OUT / f"{isrc}.mp3"
                print(f"Downloading {link} -> {dst}")
                urllib.request.urlretrieve(link, str(dst))
                print(f"Downloaded! Size: {dst.stat().st_size / 1024:.1f} KB")
                break
        except Exception as e:
            print(f"Error on {isrc}:", e)
