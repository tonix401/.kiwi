#!/bin/bash

if pgrep -f "hyprsunset" >/dev/null; then
  echo '{"text": "󰃟", "tooltip": "Nightlight is on", "class": "on"}'
else
  echo '{"text": "󰃞", "tooltip": "Nightlight is off", "class": "off"}'
fi