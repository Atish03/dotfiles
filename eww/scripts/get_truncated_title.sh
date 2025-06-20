#! /bin/bash

TITLE=$(playerctl metadata --format "{{title}}")
TRUNC_TITLE=$(echo $TITLE | cut -b 1-18)

if [[ "$TITLE" != "$TRUNC_TITLE" ]]; then
  TRUNC_TITLE="$TRUNC_TITLE ..."
fi

echo $TRUNC_TITLE
