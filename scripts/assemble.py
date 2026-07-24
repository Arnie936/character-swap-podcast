#!/usr/bin/env python3
"""assemble.py — Finaler Schnitt fuer Character-Swap-Podcast-Videos.

Fuegt Clips in Reihenfolge zusammen:
- Rolle "wide"  : Vollbild (z. B. Intro mit beiden Figuren)
- Rolle "left"  : Punch-in auf die Figur links im Bild (KI-Clips)
- Rolle "right" : Punch-in auf den Menschen rechts im Bild (Nutzer-Clips)

Alle Clips werden auf 1920x1080 / 24 fps gebracht, per loudnorm auf
einheitliche Lautstaerke gezogen und mit Crossfades (Bild + Ton)
verbunden.

Beispiel:
  python assemble.py -o "Finales Video.mp4" \
    --clip "0 Intro mit Figur.mp4:wide" \
    --clip "KI Clip 1.mp4:left" \
    --clip "1 Sprechvideo.mp4:right" \
    --clip "KI Clip 2.mp4:left"

Crop-Werte vorher anhand eines Stichproben-Frames pruefen (Gesicht muss
im Ausschnitt liegen) und bei Bedarf per --crop-left / --crop-right
anpassen (Format w:h:x:y, bezieht sich auf die Quellaufloesung).
"""

import argparse
import json
import subprocess
import sys


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_type",
         "-of", "json", path],
        capture_output=True, text=True, check=True)
    data = json.loads(out.stdout)
    has_audio = any(s.get("codec_type") == "audio" for s in data.get("streams", []))
    return float(data["format"]["duration"]), has_audio


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-o", "--output", required=True)
    p.add_argument("--clip", action="append", required=True,
                   help="datei.mp4:wide|left|right (mehrfach, in Reihenfolge)")
    p.add_argument("--crop-left", default="853:480:0:90",
                   help="Punch-in links, Default fuer 720p-KI-Clips (w:h:x:y)")
    p.add_argument("--crop-right", default="1280:720:640:40",
                   help="Punch-in rechts, Default fuer 1080p-Nutzer-Clips (w:h:x:y)")
    p.add_argument("--fade", type=float, default=0.5, help="Crossfade-Dauer in s")
    p.add_argument("--crf", default="18")
    args = p.parse_args()

    clips = []
    for spec in args.clip:
        path, _, role = spec.rpartition(":")
        if role not in ("wide", "left", "right") or not path:
            p.error(f"Ungueltiges --clip-Format: {spec!r} (erwartet datei.mp4:wide|left|right)")
        dur, has_audio = probe(path)
        if not has_audio:
            p.error(f"Clip hat keinen Ton: {path}")
        clips.append((path, role, dur))

    crops = {"left": args.crop_left, "right": args.crop_right}
    t = args.fade
    n = len(clips)

    inputs = []
    for path, _, _ in clips:
        inputs += ["-i", path]

    chains = []
    for i, (_, role, _) in enumerate(clips):
        vf = "fps=24,"
        if role in crops:
            vf += f"crop={crops[role]},"
        vf += "scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p"
        chains.append(f"[{i}:v]{vf}[v{i}]")
        chains.append(
            f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"loudnorm=I=-16:TP=-1.5:LRA=11[a{i}]")

    # xfade-Offsets: offset_k = Summe(dur_0..k) - (k+1)*t
    cum = 0.0
    for k in range(n - 1):
        cum += clips[k][2]
        offset = cum - (k + 1) * t
        src = "[v0]" if k == 0 else f"[x{k}]"
        dst = f"[x{k + 1}]"
        chains.append(f"{src}[v{k + 1}]xfade=transition=fade:duration={t}:offset={offset:.3f}{dst}")
        asrc = "[a0]" if k == 0 else f"[aa{k}]"
        adst = f"[aa{k + 1}]"
        chains.append(f"{asrc}[a{k + 1}]acrossfade=d={t}:c1=tri:c2=tri{adst}")

    filter_complex = ";".join(chains)
    total = sum(d for _, _, d in clips) - (n - 1) * t

    cmd = (["ffmpeg", "-y", "-v", "error"] + inputs +
           ["-filter_complex", filter_complex,
            "-map", f"[x{n - 1}]", "-map", f"[aa{n - 1}]",
            "-c:v", "libx264", "-preset", "medium", "-crf", args.crf,
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            args.output])
    subprocess.run(cmd, check=True)
    print(f"Fertig: {args.output} (ca. {total:.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
