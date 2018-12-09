# audio-analysis

Download the repository folder.

To achieve the image below ![alt text]

You can run [spectralLoudSub.py](https://github.com/amilo/audio-analysis/blob/master/spectralLoudSub.py) with [aural30sec-001-WLP-mono.wav](https://github.com/amilo/audio-analysis/blob/master/aural30sec-001-WLP-mono.wav) by typing in the terminal ``` python spectralLoudSub.py *mono.wav ```.

This will look for all wave files ending in ``` mono.wav ``` and run the script.

The script plots the spectrogram for the given file and looks for the left and right csv file of the given file removing the last part ```*abcd.wav```.

This is because sonic-annotator transforms a given file in output ``` filetitle.wav_vamp_vamp-libxtract_loudness_loudness.csv ```.

Therefore, we clean the termination and read the already generated files for left and right channel. The script takes the data an plots the loudness representation above the spectrogram, plotting the difference between left and right channel, on the Y = 0 axis.

The modularity might work better generating the files to be analysed with the [following sox script](https://github.com/amilo/audio-analysis/blob/master/split-and-mix.sh)(create yourfolder first, or sox will complain).

``` 
#!/bin/bash

for f in *.wav;  
do 
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-left.wav" remix 1  
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-righ.wav" remix 2  
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-mono.wav" remix 1,2  
  
done  
```
To generate the files with sonic-annotator you need to use a transform file ``` loudness.n3``` like [this](https://github.com/amilo/audio-analysis/blob/master/loudness.n3) and run

``` 
#!/bin/bash

for f in *.wav;
do
  sonic-annotator -t loudness.n3 "$f" -w csv
done
``` 
as in this [file](https://github.com/amilo/audio-analysis/blob/master/runLoudness.sh).

Remember to make the scripts executable ``` chmod +x scriptName.sh``` .

[img]: aural30sec-001-WLP-mono-Subtraction.png "Example Image"
