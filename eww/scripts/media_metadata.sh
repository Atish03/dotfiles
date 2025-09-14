#! /bin/bash

IGNORED_PLAYERS="kdeconnect,"

CURRENT_METADATA=$(playerctl --ignore-player=$IGNORED_PLAYERS metadata 2>&1)
TITLE=$($HOME/.config/eww/scripts/get_truncated_title.sh | sed -e "s/\"/'/g")
ARTIST=$(playerctl --ignore-player=$IGNORED_PLAYERS metadata --format "{{artist}}")
COVER_URL=$((playerctl --ignore-player=$IGNORED_PLAYERS metadata 2>/dev/null || echo 'artUrl: file://'$HOME'/.config/eww/images/default_cover.png') | awk '/artUrl/' | rev | cut -d ' ' -f 1 | rev)
PROGRESS=$( playerctl --ignore-player=$IGNORED_PLAYERS metadata --format "{{100*(position/mpris:length)}}" 2>/dev/null || echo 0)
OUTPUT=$($HOME/.config/eww/scripts/audio.py)

# if [[ "$TITLE" == "" || "$CURRENT_METADATA" == "No players found" ]]; then
#   TITLE="NO TITLE"
# fi
#
# if [[ "$ARTIST" == "" || "$CURRENT_METADATA" == "No players found" ]]; then
#   ARTIST="XD"
# fi
#
# if [[ "$COVER_URL" == "" || "$CURRENT_METADATA" == "No players found" ]]; then
#   COVER_URL="file:///$HOME/.config/eww/images/default_cover.png"
# fi
#
# if [[ "$PROGRESS" == "" || "$CURRENT_METADATA" == "No players found" ]]; then
#   PROGRESS="0"
# fi

printf '{"title": "%s", "artist": "%s", "cover_url": "%s", "progress": %s, "output": %s}\n' "$TITLE" "$ARTIST" "$COVER_URL" "$PROGRESS" "$OUTPUT"
