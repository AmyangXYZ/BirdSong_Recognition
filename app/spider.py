#coding=utf-8
import requests, os, sys, re
from pydub import AudioSegment
from tqdm import tqdm

def GetBirds():
    url = 'http://sound.niaolei.org.cn/'
    birds = re.findall(r'</i></a>:<a href=\"(.*)\" target=\"_blank\" title="(.*)的叫声" class="baikelink\">',requests.get(url).content)
    return birds

def DownloadMP3(data_path):
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    rep = requests.get(url)
    htmls = re.findall(r'<a target="_blank" title="点击播放" href=\"(.*)\">第',rep.content)

    mp3 = []
    for i in htmls:
        rep1 = requests.get(i)
        mp3.append(re.findall(r'mp3:\"(.*)\"',rep1.content)[0])


    for i in tqdm(range(0,len(mp3))):
        with open(data_path+str(i)+'.mp3','wb+') as f:
            f.write(requests.get(mp3[i]).content)

    return 0

def mp3_to_wav(data_path):
    for mp3file in sorted([x for x in os.listdir(data_path) if x.endswith('.mp3')]):
        try:
            sound = AudioSegment.from_mp3(data_path+mp3file)
            sound.export(data_path+mp3file.split('.')[0]+'.wav', format="wav")
        except:
            print '\t' + mp3file + ' error'
        os.remove(data_path + mp3file)
    return 0

if __name__ == "__main__":
    birds = GetBirds()
    print '[*] birds list:\n\t',
    for bird, id in zip(birds,range(0,len(birds))):
        print '{} - {}, '.format(id,bird[1]),
    print

    for url, bird in birds[11:]:
        data_path = '/srv/flask/BirdSong_Recognition/app/data/' + bird + '/'
        print '[*] downloading {}\'s songs ({})...'.format(bird,url)

        DownloadMP3(data_path)
        mp3_to_wav(data_path)
