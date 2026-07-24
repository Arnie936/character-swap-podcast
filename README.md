# Character Swap Podcast — Skill für Coding-Agents

Erstelle Podcast-Videos, in denen **du ein Gespräch mit einer KI-Figur führst**
(Anime-Charakter, Alien, Roboter …): Du filmst dich allein mit einem leeren
Sessel neben dir — der Skill fügt die Figur ein, lässt sie mit deutscher
Stimme und Lipsync auf deine Zeilen antworten und schneidet alles zu einem
fertigen Video mit Sprecher-Fokus und weichen Übergängen zusammen.

## Schnellstart: Prompt zum Kopieren

Gib das einfach deinem Coding-Agenten (Kimi Code, Claude Code, Codex o. ä.):

```text
Klone das Repository https://github.com/Arnie936/character-swap-podcast in
mein Skills-Verzeichnis (z. B. ~/.agents/skills/ oder ~/.claude/skills/ —
prüfe, welches Verzeichnis du für Skills nutzt), sodass der Ordner
"character-swap-podcast" mit der SKILL.md dort liegt. Lies danach die
SKILL.md und erkläre mir Schritt für Schritt, was ich tun muss, um mein
erstes Character-Swap-Podcast-Video zu erstellen.
```

Das reicht: Der Agent installiert den Skill damit, führt dich durch Setup,
Drehbuch, Dreh-Anleitung, Generierung und Schnitt.

## Danach: So startest du ein Video

Sag deinem Agenten z. B.:

> „Ich will ein Podcast-Video machen, in dem ich mit einer Anime-Frau
> diskutiere. Führ mich durch."

Der Skill fragt dich dann nach Drehbuch (oder hilft beim Schreiben),
Charakter und führt dich durch den Rest.

## Was der Skill automatisiert

- **Setup-Check:** prüft/installiert ffmpeg und die Higgsfield CLI, hilft bei
  der Anmeldung (siehe Hinweis unten)
- **Drehbuch:** Regeln und Vorlage für den I:/KI:-Dialog inkl. Timing-Grenzen
- **Dreh-Anleitung:** wie du dein Footage filmst (leerer Sessel, Blickrichtung,
  Clip-Nummerierung)
- **Generierung:** Figur einfügen mit Seedance 2.0, sprechende Antwort-Clips
  mit Gemini Omni Flash — alle Clips konsistent über ein Referenz-Frame
- **Schnitt:** ffmpeg-Pipeline mit Punch-ins auf den jeweiligen Sprecher,
  Crossfades und Lautheits-Normalisierung (1080p/24 fps)

## Voraussetzungen

- Ein Rechner mit **ffmpeg**, **Python 3** und der **Higgsfield CLI**
  (der Skill prüft das alles und installiert, was fehlt)
- Ein **Higgsfield-Account** mit Credits (die Videogenerierung kostet Credits,
  der Skill fragt vor jeder Ausgabe um Freigabe)
- Dein eigenes Talking-Head-Footage — oder du folgst der Dreh-Anleitung im Skill

## Repo-Struktur

```
character-swap-podcast/
├── SKILL.md                  # Der geführte Workflow (Setup → Drehbuch → Dreh → Generierung → Schnitt)
├── references/
│   ├── characters.md         # Charakter-Vorlagen (Anime-Frau, Alien, Roboter, Custom)
│   └── drehbuch.md           # Drehbuch-Regeln und Timing-Grenzen
├── scripts/
│   ├── ki_clip.sh            # KI-Antwort-Clip erzeugen (Gemini Omni Flash)
│   └── assemble.py           # Finaler Schnitt (Punch-ins, Crossfades, Loudnorm)
└── evals/                    # Test-Prompts für Skill-Evaluierungen
```

## Hinweis zum Affiliate-Link

Der Skill enthält in der Setup-Phase (`SKILL.md`, Phase 0) einen
Affiliate-Link für die Higgsfield-Registrierung. Wenn du dich darüber
anmeldest, bekommt der Autor eine kleine Provision — für dich entstehen
keine Mehrkosten. Du kannst dich natürlich auch direkt bei Higgsfield
anmelden, der Skill funktioniert identisch.
