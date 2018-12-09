# audio-analysis

You can run it with <code> python spectralLoudSub.py *mono.wav </code>

and will look for all wave files ending in <code> mono.wav </code> and run the script.

The script plots the spectrogram for the given file and looks for the left and right csv file from the suffix *abcd.wav.

This is because sonic-annotator transforms outputs <code> filetitle.wav_vamp_vamp-libxtract_loudness_loudness.csv </code>.

Therefore, we clean the termination.

This might work better generating the files with the following sox script (create yourfolder first, or sox will complain).

<code> 

#!/bin/bash

for f in *.wav;
do
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-left.wav" remix 1
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-righ.wav" remix 2
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-mono.wav" remix 1,2

done
</code>
