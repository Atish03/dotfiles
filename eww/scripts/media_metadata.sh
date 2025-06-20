#! /bin/bash

CURRENT_METADATA=$(playerctl metadata 2>&1)
TITLE=$($HOME/.config/eww/scripts/get_truncated_title.sh | sed -e "s/\"/'/g")
ARTIST=$(playerctl metadata --format "{{artist}}")
COVER_URL=$(playerctl metadata | awk '/artUrl/' | rev | cut -d ' ' -f 1 | rev)
PROGRESS=$(playerctl metadata --format "{{100*(position/mpris:length)}}")
OUTPUT=$($HOME/.config/eww/scripts/audio.py)

if [[ "$TITLE" == "" || "$CURRENT_METADATA" == "No players found" ]]; then
  TITLE="NO TITLE"
fi

if [[ "$ARTIST" == "" || "$CURRENT_METADATA" == "No players found" ]]; then
  ARTIST="XD"
fi

if [[ "$COVER_URL" == "" || "$CURRENT_METADATA" == "No players found" ]]; then
  COVER_URL="file:///$HOME/.config/eww/images/default_cover.png"
fi

if [[ "$PROGRESS" == "" || "$CURRENT_METADATA" == "No players found" ]]; then
  PROGRESS="0"
fi

printf '{"title": "%s", "artist": "%s", "cover_url": "%s", "progress": %s, "output": %s}\n' "$TITLE" "$ARTIST" "$COVER_URL" "$PROGRESS" "$OUTPUT"
