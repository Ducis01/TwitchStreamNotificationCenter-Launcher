#!/bin/bash
/usr/bin/say "Lanching" $1 "Stream" &
exec $2 -p $3 --player-args "--title='$4' {filename}" twitch.tv/$1 source --hls-live-edge 10 --hls-segment-threads 2
