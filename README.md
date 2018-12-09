# audio-analysis

Download the repository folder.

To achieve the image below ![alt text][img]

Make sure you have a stereo wav file in the folder, like the example ```aural30sec-001-WLP.wav```.
Make the scripts executable ``` $ chmod +x split-and-mix.sh``` . 

Run in the terminal

``` $ split-and-mix.sh ```

This will take all the wav files in the repository folder and generate in ``` yourfolder```  the wav files to be analysed in sonic-annotator. The [script](https://github.com/amilo/audio-analysis/blob/master/split-and-mix.sh) uses [sox](http://sox.sourceforge.net/), so you will have to install this first, for example ```brew install sox```.

The script will create a mono mixed 16bit version of your stereo file and split the channels in left and right.
The naming ```righ``` is for string uniformity.

``` 
#!/bin/bash

for f in *.wav;  
do 
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-left.wav" remix 1  
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-righ.wav" remix 2  
  sox "$f" -b 16 "yourfolder/${f:0:${#f}-4}-mono.wav" remix 1,2  
  
done  
```
Now move to ``` yourfolder``` :
``` $ cd yourfolder``` 

You have now two choices: (i) you generate new csv [below](#generate-csv) (ii) you [test](#csv-already-generated) the script with the existing csv.

# Generate CSV

To generate the files with sonic-annotator you need to use a transform file ``` loudness.n3``` like [this](https://github.com/amilo/audio-analysis/blob/master/loudness.n3) and run the following script, that you can find also [here](https://github.com/amilo/audio-analysis/blob/master/runLoudness.sh). You will need to have [sonic-annotator](https://code.soundsoftware.ac.uk/projects/sonic-annotator/wiki) installed. Remember again to make the batch wav file script executable ``` $ chmod +x runLoudness.sh``` or apply the transorm individually ``` $ sonic-annotator -t loudness.n3 *.wav -w csv```. You can use ``` $ sonic-annotator -t loudness.n3 *.wav -w csv --csv-force``` if you are overwiting files.

``` 
#!/bin/bash

for f in *.wav;
do
  sonic-annotator -t loudness.n3 "$f" -w csv
done
``` 

# CSV already generated

After generating the files, or to test this example, you can run [spectralLoudSub.py](https://github.com/amilo/audio-analysis/blob/master/spectralLoudSub.py) with [aural30sec-001-WLP-mono.wav](https://github.com/amilo/audio-analysis/blob/master/aural30sec-001-WLP-mono.wav) by typing in the terminal ``` python spectralLoudSub.py *mono.wav ```.

This will look for all wave files ending in ``` mono.wav ``` and run the script.

The script plots the spectrogram for the given file and looks for the left and right csv file of the given file removing the last part ```*abcd.wav```.

This is because sonic-annotator transforms a given file in output ``` filetitle.wav_vamp_vamp-libxtract_loudness_loudness.csv ```.

Therefore, we clean the termination and read the already generated files for left and right channel. The script takes the data an plots the loudness representation above the spectrogram, plotting the difference between left and right channel, on the Y = 0 axis.


[img]: aural30sec-001-WLP-mono-Subtraction.png "Example Image"
