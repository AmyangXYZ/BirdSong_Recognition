# BirdSong Recognition

## A Flask Web Application for Birdsong Recognition.

Our school is at the foot of the mountain, every day the school is filled with beautiful birdsong, but we do not know their names. So we have an idea of making a birdsong recognition application.

It has 22 kinds of bird now,
the correct rate is: 81.8% (with only 1.7G data trained).

## Steps:

+   Load & Preprocess audio
+   Etract MFCCs Feature
+   Build & Train Model
+   Deploy on the server
  
## Note:

Due to my careless, some path values are set in many files, please just use some cmd to replace them, e.g. `sed -i "s/\/home\/amyang\/Projects/\/root/g" `grep /home/amyang/Projects -rl ./*`` (here `root` is the new path)
