# audio-analysis

You can run it with ``` python spectralLoudSub.py *mono.wav ```

and will look for all wave files ending in ``` mono.wav ``` and run the script.

The script plots the spectrogram for the given file and looks for the left and right csv file from the suffix ```*abcd.wav```.

This is because sonic-annotator transforms outputs ``` filetitle.wav_vamp_vamp-libxtract_loudness_loudness.csv ```.

Therefore, we clean the termination.

This might work better generating the files with the [following sox script](https://github.com/amilo/audio-analysis/blob/master/split-and-mix.sh)(create yourfolder first, or sox will complain).

``` #!/bin/bash</code>
  
for f in *.wav;  
do 
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-left.wav" remix 1  
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-righ.wav" remix 2  
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-mono.wav" remix 1,2  
  
done  
```
