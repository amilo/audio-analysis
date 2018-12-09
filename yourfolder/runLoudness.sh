#!/bin/bash

for f in *.wav;
do
  sonic-annotator -t loudness.n3 "$f" -w csv
done
