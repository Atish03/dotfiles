#!/bin/bash

pactl set-default-sink "$(pactl list sinks | grep -C1 -ie "$(pactl list sinks | grep -ie "description:" | cut -d: -f2 | sort | env -C $HOME rofi -dmenu -theme .config/rofi/wifimenu/theme.rasi)" | grep Name | cut -d: -f2 | xargs)"
