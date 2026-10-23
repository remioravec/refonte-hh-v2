import json, os, re, subprocess, sys, time, urllib.request

KEY = os.environ["ELEVENLABS_API_KEY"]
VOICE = "cjVigY5qzO86Huf0OWal"
PROJ = "/home/user/refonte-hh-v2/videos/hello-harel-promo"

lines = re.findall(r"\n    (\S.*)", open(f"{PROJ}/SCRIPT.md").read())
meta = json.load(open(f"{PROJ}/audio_meta.json"))
have = {v["frame"] for v in meta["voices"]}
missing = [i for i in range(1, len(lines) + 1) if i not in have]
print("manquantes:", missing)

for n in missing:
    text = lines[n - 1]
    body = json.dumps({
        "text": text, "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.45, "similarity_boost": 0.80,
                           "style": 0.15, "use_speaker_boost": True},
    }).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}",
        data=body, headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    mp3 = f"/tmp/hh-{n:02d}.mp3"
    wav = f"{PROJ}/assets/voice/{n:02d}.wav"
    for essai in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                open(mp3, "wb").write(r.read())
            break
        except Exception as e:
            print(f"  ligne {n} essai {essai+1} KO: {e}")
            time.sleep(4 * (essai + 1))
    else:
        print(f"  ligne {n} ABANDON"); continue
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3,
                    "-ac", "1", "-ar", "44100", wav], check=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of", "csv=p=0", wav],
                               capture_output=True, text=True).stdout.strip())
    meta["voices"].append({"frame": n, "path": f"assets/voice/{n:02d}.wav",
                           "duration_s": round(dur, 3), "words": []})
    os.remove(mp3)
    print(f"  ligne {n} ok -> {dur:.3f}s")
    time.sleep(2)

meta["voices"].sort(key=lambda v: v["frame"])
json.dump(meta, open(f"{PROJ}/audio_meta.json", "w"), indent=2, ensure_ascii=False)
print("total voix:", len(meta["voices"]),
      "| duree", round(sum(v["duration_s"] for v in meta["voices"]), 2), "s")
