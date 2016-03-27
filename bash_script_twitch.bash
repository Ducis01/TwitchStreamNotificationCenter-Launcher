#!/bin/bash

say "Lanching" $1 "Stream" &
$2 -p $3 twitch.tv/$1 source --hls-live-edge 10 --hls-segment-threads 2
say "End of stream"