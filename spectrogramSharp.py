#!/usr/bin/env python
#coding: utf-8
""" This work is licensed under a Creative Commons Attribution 3.0 Unported License.
    Frank Zalkow, 2012-2013 """

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import pyplot as figure
import scipy.io.wavfile as wav
from numpy.lib import stride_tricks
import sys
# import wavio
import csv
plt.rcParams.update({'font.size': 10})




""" short time fourier transform of audio signal """
def stft(sig, frameSize, overlapFac=0.5, window=np.hanning):
    win = window(frameSize)
    # hopSize = int(frameSize - np.floor(overlapFac * frameSize))
    hopSize = int(frameSize - np.int(overlapFac * frameSize))

    # zeros at beginning (thus center of 1st window should be for sample nr. 0)
    # samples = np.append(np.zeros(np.floor(frameSize/2.0)), sig)
    samples = np.append(np.zeros(np.int(frameSize/2.0)), sig)
    # cols for windowing
    cols = np.ceil( (len(samples) - frameSize) / float(hopSize)) + 1
    # zeros at end (thus samples can be fully covered by frames)
    samples = np.append(samples, np.zeros(frameSize))

    frames = stride_tricks.as_strided(samples, shape=(cols, frameSize), strides=(samples.strides[0]*hopSize, samples.strides[0])).copy()
    frames *= win

    return np.fft.rfft(frames)

""" scale frequency axis logarithmically """
def logscale_spec(spec, sr=44100, factor=20.):
    timebins, freqbins = np.shape(spec)

    scale = np.linspace(0, 1, freqbins) ** factor
    scale *= (freqbins-1)/max(scale)
    scale = np.unique(np.round(scale))

    # create spectrogram with new freq bins
    newspec = np.complex128(np.zeros([timebins, len(scale)]))
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            newspec[:,i] = np.sum(spec[:,scale[i]:], axis=1)
        else:
            newspec[:,i] = np.sum(spec[:,scale[i]:scale[i+1]], axis=1)

    # list center freq of bins
    allfreqs = np.abs(np.fft.fftfreq(freqbins*2, 1./sr)[:freqbins+1])
    freqs = []
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            freqs += [np.mean(allfreqs[scale[i]:])]
        else:
            freqs += [np.mean(allfreqs[scale[i]:scale[i+1]])]

    return newspec, freqs

""" plot spectrogram"""
def plotstft(audiopath, binsize=2**10, plotpath=None, colormap="viridis"):

    samplerate, samples = wav.read(audiopath)
    # object = wavio.read(audiopath)
    #
    # samplerate = object.rate
    # samples = object.data
    # samplerate, width, samples = wavio.read(audiopath)
    s = stft(samples, binsize)

    sshow, freq = logscale_spec(s, factor=1.0, sr=samplerate)
    ims = 20.*np.log10(np.abs(sshow)/10e-6) # amplitude to decibel

    timebins, freqbins = np.shape(ims)


    # ax1 = fig.add_subplot(2,1,1)
    # fig = plt.figure(figsize=(15, 7.5))
    # figure(num=None, figsize=(15, 7), dpi=150, facecolor='w', edgecolor='k')
    fig, axes = plt.subplots(nrows=2)
    fig.set_size_inches(18.5, 10.5)

    # fig, (axes[0], axes[1]) = plt.subplots(nrows=2)

    im = axes[1].imshow(np.transpose(ims), origin="lower", aspect="auto", cmap=colormap, interpolation="none")

    # ax0.set_title('pcolormesh with levels')

    # axes[1].imshow(np.transpose(ims), origin="lower", aspect="auto", cmap=colormap, interpolation="none")

    # fig.colorbar(im, ax=axes[1])

    # axes[1].colorbar()
    # #
    plt.xlabel("time (s)")
    plt.ylabel("frequency (hz)")
    plt.xlim([0, timebins-1])
    plt.ylim([0, freqbins])



    xlocs = np.float32(np.linspace(0, timebins-1, 32))
    numx = ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate]
    xnumbers = [ int(round(float(x))) for x in numx]
    # plt.xticks(xlocs, ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
    plt.xticks(xlocs, xnumbers)

    ylocs = np.int16(np.round(np.linspace(0, freqbins-1, 11)))

    plt.yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])

    # number = file[11:24] + "sharpness"
    parsedpath = audiopath[0:len(audiopath)-4]
    print parsedpath
    csvpath = parsedpath + "_vamp_vamp-libxtract_sharpness_sharpness.csv"

    x = []
    y = []

    with open(csvpath,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(float(row[0]))
            y.append(float(row[1]))


    axes[0].plot(x, y, 200, 'r', label=audiopath, linestyle='-', linewidth=0.5, markersize=1)
    # axes[0].set_xlabel('Time (seconds)')
    axes[0].set_ylabel('Sharpness ')
    axes[0].axis([0, 31, 0, 1])

    plotpath = audiopath + ".pdf"


    if plotpath:
        # plt.savefig(plotpath, bbox_inches="tight", dpi=100)
        plt.savefig(plotpath, dpi=100)
    else:
        plt.show()

    plt.clf()


def main(files):

    for f in files:
        plotstft(f)
        print "Saving Image for ", f

if __name__ == "__main__":
    files = sys.argv[1:] # slices off the first argument (executable itself)
    main(files)
