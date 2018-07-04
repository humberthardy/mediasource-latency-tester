#!/usr/bin/env bash
# convert wav sound to the opus
docker run -v$(pwd):/audio:rw  maxmcd/gstreamer:1.14-buster gst-launch-1.0 -v filesrc location=/audio/Death_By_Unga_-_09_-_Young_Girls.wav ! wavparse ! opusenc complexity=0 frame-size=2.5  ! webmmux ! filesink location=/audio/Death_By_Unga_-_09_-_Young_Girls.webm