#!/usr/bin/env bash

function handle {
  case $1 in
    "openwindow"*) notify-send "Window opened" ;;
  esac
}

socat - "UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock" | while read -r line; do handle "$line"; done