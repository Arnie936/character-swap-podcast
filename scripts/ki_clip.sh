#!/usr/bin/env bash
# ki_clip.sh — Erzeugt einen sprechenden KI-Clip mit Gemini Omni Flash.
#
# Umgeht den CLI-Bug, dass --image/--start-image bei gemini_omni abgelehnt
# werden, indem das Referenz-Frame als rohes medias-JSON uebergeben wird.
#
# Aufruf:
#   bash ki_clip.sh <referenz_frame.png> "<prompt>" <dauer_sek> <output.mp4>
#
# Die Upload-ID des Referenz-Frames wird ueber die Umgebungsvariablen
# KI_FRAME_ID und KI_FRAME_URL gecacht — beim ersten Aufruf exportieren
# lassen oder einfach mehrfach aufrufen; das Skript laedt nur neu hoch,
# wenn die Variablen fehlen. Praktisch: nach dem ersten Lauf zeigt das
# Skript die export-Zeile an.
set -euo pipefail

FRAME="$1"
PROMPT="$2"
DUR="${3:-8}"
OUT="$4"

if [[ -z "${KI_FRAME_ID:-}" || -z "${KI_FRAME_URL:-}" ]]; then
  echo "Lade Referenz-Frame hoch: $FRAME" >&2
  UPLOAD=$(higgsfield upload create "$FRAME" --json)
  KI_FRAME_ID=$(printf '%s' "$UPLOAD" | python -c "import json,sys; print(json.load(sys.stdin)['id'])")
  KI_FRAME_URL=$(printf '%s' "$UPLOAD" | python -c "import json,sys; print(json.load(sys.stdin)['url'])")
  echo "Fuer weitere Aufrufe cachen:" >&2
  echo "  export KI_FRAME_ID=$KI_FRAME_ID" >&2
  echo "  export KI_FRAME_URL=$KI_FRAME_URL" >&2
fi

MEDIAS="[{\"role\":\"image\",\"data\":{\"id\":\"$KI_FRAME_ID\",\"type\":\"media_input\",\"url\":\"$KI_FRAME_URL\"}}]"

RESULT=$(higgsfield generate create gemini_omni \
  --prompt "$PROMPT" \
  --duration "$DUR" \
  --aspect_ratio 16:9 \
  --medias "$MEDIAS" \
  --wait --wait-timeout 20m --json)

URL=$(printf '%s' "$RESULT" | python -c "import json,sys; print(json.load(sys.stdin)[0]['result_url'])")
curl -fsSL -o "$OUT" "$URL"
echo "Fertig: $OUT"
