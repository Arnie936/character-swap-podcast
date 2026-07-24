# Drehbuch-Regeln (I:/KI:-Dialog)

## Grundstruktur

```
I:
<Zeile des Nutzers>

KI:
<Zeile der Figur>

I:
...
```

- Strikter Wechsel I → KI → I → KI. Der Nutzer dreht nur seine I-Zeilen;
  jede KI-Zeile wird später ein generierter Clip.
- **Clip 0 ist immer eine I-Zeile**: Begrüßung + Vorstellung des Gastes
  (z. B. "Heute stelle ich einen Spezialgast vor. Erzähl etwas von dir.").
  Auf diese Zeile wird in Phase 3 die Figur eingefügt — sie winkt nur,
  spricht noch nicht.
- Anzahl: 3–5 Wechsel funktionieren gut (≈ 60–90 s Endvideo).

## Timing-Grenzen (wichtig!)

- **KI-Zeilen: maximal ~9 Sekunden Sprechzeit** (Gemini Omni kann nur 10 s
  pro Clip). Faustregel: ≤ 30 deutsche Wörter pro KI-Zeile. Längere Ideen
  auf zwei aufeinanderfolgende KI-Clips aufteilen (ist im Schnitt unproblematisch,
  weil der Punch-in ohnehin auf der Figur bleibt).
- I-Zeilen: beliebig lang, aber kurze Zeilen (2–6 s) halten das Tempo hoch.
- Pausen ("...") im Text werden vom Modell tatsächlich gesprochen — sparsam
  einsetzen, sie kosten Clip-Zeit.

## Dramaturgie, die funktioniert

- Der Nutzer ist die ernste Seite, die Figur ist frech/sarkastisch/genervt.
  Konflikt > Harmonie: die Figur beschwert sich, stellt dumme Fragen oder
  dreht dem Nutzer die Argumente um.
- **Running Gag einbauen:** eine Prämisse (z. B. "du hältst mich hier
  gefangen"), die über mehrere Zeilen eskaliert — sie trägt die
  Schluss-Punchline.
- **Schluss:** optionaler Bonus-Clip der Figur nach der letzten I-Zeile
  (siehe `references/characters.md` → Punchline-Optionen). Dem Nutzer immer
  2–3 Varianten zur Auswahl vorlegen, bevor generiert wird.

## Beispiel-Gerüst

```
I:  Heute stelle ich einen Spezialgast vor. Erzähl etwas von dir.
KI: <pikierte Antwort, die den Konflikt aufmacht>
I:  <ernst gemeinte Folgefrage>
KI: <Beschwerde über die reale Welt / den Nutzer>
I:  <Verteidigung>
KI: <dreht die Verteidigung um — Running Gag gipfelt>
I:  <letzte I-Zeile, optional>
KI: <Schluss-Punchline / Bonus-Clip>
```
