# BirdSong Recognition

Our school is at the foot of the mountain, every day the school is filled with beautiful birdsong, but we do not know their names. So we have an idea of making a birdsong recognition application.

It has 22 kinds of bird now, the correct rate is 81.8% (with only 1.7G data trained).

Acutally it is a isolate-word recognition problem, so We use the classic HMM+MFCC method.

## Installation

`git clone https://github.com/AmyangXYZ/BirdSong_Recognition`

`cd BirdSong_Recognition/`

`docker build -t birdsong .`

`docker run -d --name docker_birdsong -p 80:80 birdsong`

## Environment

Python3.7

Libraries: tqdm, wheel, pydub, hmmlearn, librosa, sklearn, matplotlib, scipy
