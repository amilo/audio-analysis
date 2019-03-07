#!/bin/bash

for f in *.wav;
do
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-left.wav" remix 1
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-righ.wav" remix 2
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-mono.wav" remix 1,2

done
