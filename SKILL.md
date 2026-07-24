---
name: character-swap-podcast
description: |
  Führt komplett durch die Erstellung eines "Character Swap Podcast"-Videos:
  ein reeller Mensch führt ein Interview/Gespräch mit einer KI-Figur
  (Anime-Charakter, Alien, Roboter o.ä.), die per Higgsfield in sein
  selbstgedrehtes Talking-Head-Video eingefügt wird und mit eigener Stimme
  antwortet. Der Skill deckt alles ab: Installation/Prüfung von ffmpeg und
  Higgsfield CLI (Account-Einrichtung inkl. Affiliate-Link), gemeinsame
  Drehbuch-Erstellung, Dreh-Anleitung für das Nutzer-Footage, Charakterwahl,
  Clip-Generierung mit Seedance 2.0 (Figur einfügen) und Gemini Omni Flash
  (sprechende KI-Antworten mit Lipsync auf Deutsch), Konsistenz über ein
  Referenz-Frame, Qualitätskontrolle und finaler Podcast-Schnitt mit ffmpeg
  (Punch-ins auf den jeweiligen Sprecher, Crossfades, Lautheits-Normalisierung).
  IMMER verwenden, wenn der Nutzer ein Podcast-/Interview-Video mit einer
  KI-Figur, einem "Charakter Swap", einer Anime-Person/Alien/Figur neben sich
  im Video, einem Dialog zwischen sich und einer KI, oder etwas "wie das
  Alien-Podcast-Video" bauen will — auch wenn er nur sagt "füg eine Figur in
  mein Video ein, die mit mir spricht". Nicht für: reine Untertitel/Captions
  (embedded-captions), allgemeine Higgsfield-Generierung ohne Podcast-Konzept
  (higgsfield-generate), Websites (higgsfield-website).
---

# Character Swap Podcast

Baue aus selbstgedrehtem Talking-Head-Footage des Nutzers ein Podcast-Video,
in dem eine KI-Figur neben ihm sitzt und mit ihm dialogisiert. Der Nutzer
spielt den Interviewer ("I"), die KI-Figur ist der Gast und bekommt ihre
Antworten als generierte Clips mit deutscher Stimme und Lipsync.

**Kernprinzip — Konsistenz schlägt alles:** Es gibt genau EIN
Konsistenz-Anker-Bild: das letzte Frame des generierten Intro-Clips (Clip 0).
Dieses Frame geht als Referenz in JEDEN KI-Clip. Dadurch sehen Figur, Mensch,
Sessel, Mikro und Hintergrund in allen Clips identisch aus — das ist der
Unterschied zwischen "teuer wirkend" und "zusammengestückelt".

**Sprache:** Mit dem Nutzer Deutsch sprechen. Prompts an die Modelle auf
Englisch formulieren, die gesprochenen Dialogzeilen im Prompt auf Deutsch
(in einfachen Anführungszeichen).

## Ablauf (Phasen strikt in dieser Reihenfolge)

### Phase 0 — Setup-Check

Prüfe in dieser Reihenfolge und installiere nur, was fehlt:

1. **ffmpeg:** `ffmpeg -version`. Fehlt es: Nutzer fragen, ob installiert
   werden darf (Windows: `winget install ffmpeg` oder Hinweis auf builds von
   gyan.dev; dann PATH-Neustart beachten).
2. **Higgsfield CLI:** `higgsfield --version`. Fehlt sie:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh
   ```
3. **Account:** `higgsfield account status`. Bei `Not authenticated` /
   `Session expired`:
   - Hat der Nutzer noch KEINEN Higgsfield-Account, schicke ihn zuerst über
     diesen Affiliate-Link zur Anmeldung:
     **https://higgsfield.ai/s/mcp-arnold-oberleiter-tNjMkM**
   - Danach: `higgsfield auth login` (interaktiv, Nutzer muss selbst
     bestätigen) und auf seine Bestätigung warten.
   - Zeige danach Plan und Credit-Stand aus `account status` — der Nutzer
     soll wissen, dass Generierungen Credits kosten.
4. **Hyperframes (optional):** nur prüfen/installieren, wenn der Nutzer den
   Schnitt damit statt mit ffmpeg will. Der Standard-Schnittweg dieses
   Skills ist ffmpeg (Phase 6), dafür ist Hyperframes nicht nötig.

### Phase 1 — Interview (max. 4 Fragen pro Runde, nur Lücken abfragen)

1. **Drehbuch:** Hat der Nutzer schon eines (I:/KI:-Zeilen)? Wenn nein:
   gemeinsam nach `references/drehbuch.md` erstellen. Wenn ja: prüfen, dass
   jede KI-Zeile gesprochen ≤ ~9 Sekunden ist (sonst Zeile teilen — Gemini
   Omni kann max. 10 s pro Clip).
2. **Charakter:** Vorschläge aus `references/characters.md` zeigen
   (Anime-Frau, Alien, Roboter, Custom). Der Charakter bleibt für das ganze
   Video fix — keine nachträglichen Wechsel.
3. **Footage:** Hat der Nutzer seine Clips schon gedreht? Wenn nein →
   Dreh-Anleitung aus Phase 2 geben und stoppen, bis die Dateien da sind.
4. **Kosten-Go:** Kurz auflisten, was generiert wird (1 Seedance-Clip +
   N Gemini-Omni-Clips), und auf explizites OK warten, bevor Credits
   ausgegeben werden.

### Phase 2 — Nutzer-Footage (Dreh-Anleitung oder Check)

Wenn der Nutzer noch drehen muss, gib ihm diese Anleitung:

- **16:9, 1080p**, statische Kamera, dunkler/neutraler Hintergrund.
- Er sitzt **rechts** im Bild mit Mikro, **links** steht ein **leerer
  Sessel/Stuhl** — dort wird die Figur eingefügt. Zwischen ihm und Sessel
  etwas Raum lassen.
- **Jede I-Zeile des Drehbuchs als eigener Clip**, Dateien durchnummeriert:
  `0 Intro.mp4`, `1 ....mp4`, `2 ....mp4` … in Drehbuch-Reihenfolge.
  Clip 0 ist die Begrüßung/Vorstellung des Gastes.
- Beim Sprechen **Blick Richtung leerem Sessel**, kurze Sprechpausen am
  Clip-Anfang und -Ende (erleichtert den Schnitt).

Wenn das Footage schon existiert: mit `ffprobe` Dauer/Auflösung/FPS aller
Clips prüfen und je Clip ein Stichproben-Frame ansehen (Sitzposition,
Blickrichtung, freier Platz für die Figur). Abweichungen vom Standard-Setup
(links/rechts vertauscht etc.) früh ansprechen — Crops in Phase 6 hängen
davon ab.

### Phase 3 — Clip 0: Figur einfügen (Seedance 2.0)

Genau EIN Job fügt die Figur ins Geschehen ein:

```bash
higgsfield generate create seedance_2_0 \
  --prompt "<Charakter-Prompt aus references/characters.md>: keep the man on the right, his appearance, his original German speech and the original audio track exactly unchanged. <CHARAKTER> is now sitting in the previously empty chair on the left. <ER/SIE> smiles and waves friendly at the camera. <ER/SIE> does not speak and makes no sound. Podcast setting, dark curtain backdrop, consistent soft lighting, static camera, 16:9." \
  --video "0 Intro.mp4" \
  --duration <Sekunden des Originals, aufgerundet> \
  --resolution 1080p --aspect_ratio 16:9 \
  --wait --wait-timeout 20m --json
```

- Ergebnis-URL aus dem JSON (`result_url`) mit `curl -fsSL -o` herunterladen.
- **Sofort danach das Konsistenz-Anker-Frame extrahieren:**
  ```bash
  ffmpeg -y -v error -sseof -0.1 -i "Clip0-ergebnis.mp4" -frames:v 1 "_ref/last_frame.png"
  ```
- Ergebnis visuell prüfen (Frame ansehen): Figur sitzt im Sessel, winkt,
  Nutzer unverändert? Wenn der Take schlecht ist, dem Nutzer sagen und mit
  Kostenhinweis um Freigabe für einen Re-Roll fragen — nicht still
  weiterrechnen.

### Phase 4 — KI-Antwort-Clips (Gemini Omni Flash)

Für JEDE KI-Zeile des Drehbuchs ein Clip. Modell: `gemini_omni`
("Gemini Omni Flash"). Wichtige, erprobte Rahmenbedingungen:

- **Limits:** nur 720p, max. **10 s** Dauer, 16:9. Längere Zeilen auf zwei
  Clips aufteilen (Drehbuch-Phase sollte das verhindern).
- **CLI-Bug-Workaround (Stand higgsfield CLI 0.2.1):** Die Flags `--image`
  und `--start-image` werden bei `gemini_omni` vom Server abgelehnt
  (Validierungsfehler `GeminiOmniReferenceImageMedia.role`). Stattdessen das
  Referenz-Frame einmal hochladen und `medias` als rohes JSON übergeben:
  ```bash
  higgsfield upload create _ref/last_frame.png --json   # -> id + url merken, einmalig
  higgsfield generate create gemini_omni \
    --prompt "..." \
    --duration 8 --aspect_ratio 16:9 \
    --medias '[{"role":"image","data":{"id":"<UPLOAD_ID>","type":"media_input","url":"<UPLOAD_URL>"}}]' \
    --wait --wait-timeout 20m --json
  ```
  Das fertige Skript `scripts/ki_clip.sh` kapselt Upload + Generierung +
  Download; die Upload-ID wird über Umgebungsvariablen wiederverwendet, damit
  nicht jeder Clip neu hochlädt. Aufruf:
  ```bash
  bash scripts/ki_clip.sh "_ref/last_frame.png" "<prompt>" 8 "KI Clip 1.mp4"
  ```
  (Falls eine neuere CLI-Version `--image` akzeptiert, darf das Flag direkt
  genutzt werden — das Skript bleibt trotzdem der sichere Weg.)
- **Prompt-Vorlage pro Clip** (Englisch, deutsche Zeile in '…'):
  ```
  The <CHARAKTER> on the left speaks in German with a <EMOTION> female/male
  voice, natural lip sync and expressive facial animation:
  '<DEUTSCHE ZEILE>'. <EINE passende Geste, z.B. rolls eyes, points at the
  man, crosses arms>. The man on the right with headphones listens silently
  and does not speak. Static camera, podcast setting, dark curtain backdrop,
  keep both characters and the scene exactly consistent with the reference
  image, 16:9.
  ```
  Pro Zeile EINE klare Emotion und EINE Geste wählen, die zum Text passt —
  das macht die Figur lebendig, ohne dass das Modell überladen wird.
- **Parallelisieren:** Mehrere Clips können als parallele Hintergrund-Jobs
  laufen. Jeden Job mit `--wait --json` laufen lassen und die `result_url`
  speichern; Validierungsfehler kommen sofort, Generierung dauert wenige
  Minuten.
- **Dauer je Clip:** gesprochene Zeilenlänge + ~1 s Puffer, aufgerundet
  (typisch 6–10).

### Phase 5 — Qualitätskontrolle

Vor dem Schnitt jeden Clip prüfen:

- 2–3 Stichproben-Frames extrahieren und ansehen: gleiche Figur, gleicher
  Mensch, keine Artefakte, Geste passt?
- Tonpegel prüfen: `ffmpeg -i clip.mp4 -af volumedetect -f null /dev/null`
  (Stille = kaputt).
- Den Nutzer die Clips **anhören lassen**: Wortlaut, Stimmlage, Tempo.
  Erst Re-Rolls mit angepasstem Prompt anbieten, wenn der Nutzer moniert
  (Credits!).

### Phase 6 — Schnitt (ffmpeg, via scripts/assemble.py)

Der Standard-Look: **Intro ungeschnitten (beide im Bild), danach immer der
Sprecher im Fokus** (Punch-in), Übergänge als Crossfade:

```bash
python scripts/assemble.py -o "Finales Video.mp4" \
  --clip "Clip0-ergebnis.mp4:wide" \
  --clip "KI Clip 1.mp4:left" \
  --clip "1 Sprechvideo.mp4:right" \
  --clip "KI Clip 2.mp4:left" \
  ...
```

- `wide` = Vollbild, `left` = Punch-in auf die Figur links, `right` =
  Punch-in auf den Menschen rechts.
- Das Skript rechnet alle Clips auf 1080p/24 fps, normalisiert die
  Lautstärke (loudnorm) und setzt 0,5-s-Crossfades in Bild und Ton.
- **Crop-Koordinaten nicht blind übernehmen:** Vor dem Schnitt je einen
  Frame eines KI-Clips und eines Nutzer-Clips ansehen und prüfen, ob die
  Standard-Crops (`--crop-left 853:480:0:90` für 720p-KI-Clips,
  `--crop-right 1280:720:640:40` für 1080p-Nutzer-Clips) Gesicht und Geste
  sauber einfangen. Bei anderem Setup (Person links, engerer Ausschnitt …)
  Werte anpassen.
- Danach Stichproben an jedem Übergang und jeder Szenenmitte prüfen und das
  Ergebnis dem Nutzer zeigen. Anpassungen (engerer Zoom, längere Fades) sind
  Parameteränderungen + Neu-Render (~1 Minute).

## Grundsätze

- Keine Credits ohne explizite Freigabe ausgeben (Phase 1 und jeder Re-Roll).
- Ein Anker-Frame für alle KI-Clips — nie zwischendrin die Referenz wechseln.
- Der Mensch im Video darf durch die Generierung nicht verändert werden;
  jedes Prompt sagt das explizit.
- Fehlschläge ehrlich melden (Drift, abgelehnte Prompts, kaputter Ton),
  nicht überspielen.
- Zwischenstände (Frames, Referenzbilder) in einem Unterordner wie `_ref/`
  halten, damit der Projektordner sauber bleibt.

## Dateien

- `references/characters.md` — Charakter-Vorlagen mit Seedance-Prompt-Bausteinen
  und Stimm-/Gesten-Hinweisen für die KI-Clips.
- `references/drehbuch.md` — Regeln und Vorlage für das I:/KI:-Drehbuch,
  inkl. Timing-Grenzen und Punchline-Tricks.
- `scripts/ki_clip.sh` — Gemini-Omni-Clip erzeugen (Upload-Workaround,
  Generierung, Download in einem Aufruf).
- `scripts/assemble.py` — finaler Schnitt: Punch-ins, Crossfades, Loudnorm,
  1080p/24 fps.
