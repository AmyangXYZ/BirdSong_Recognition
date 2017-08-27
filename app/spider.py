#coding=utf-8
import requests, os, re
from pydub import AudioSegment
from tqdm import tqdm
from sql import Intro

def GetBirds():
    url = 'http://sound.niaolei.org.cn/'
    birds = re.findall(r'</i></a>:<a href=\"(.*)\" target=\"_blank\" title="(.*)的叫声" class="baikelink\">',requests.get(url).content)
    return birds

def GetIntro():
    rep = requests.get(url)
    html = re.findall(r'<a target="_blank" title="点击播放" href=\"(.*)\">第',rep.content)[0]
    intro = re.findall(u'</a>简介：(.*)>>',requests.get(html).content.decode('utf-8'))[0]
    return intro

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
        with open(data_path+str(i)+'p'+'.mp3','wb+') as f:
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
    # birds = GetBirds()
    # print '[*] birds list:\n\t',
    # for bird, id in zip(birds,range(0,len(birds))):
    #     print '{} - {}, '.format(id,bird[1]),
    # print

    data_path = u'/srv/flask/BirdSong_Recognition/app/data/灰斑鸠/'
    url = 'http://sound.niaolei.org.cn/Streptopelia-decaocto.html'
    DownloadMP3(data_path)
    mp3_to_wav(data_path)

    # for url, bird in birds[73:]:
    #     data_path = '/srv/flask/BirdSong_Recognition/app/data/' + bird + '/'
    #     print '[*] downloading {}\'s songs ({})...'.format(bird,url)
    #     try:
    #         DownloadMP3(data_path)
    #         mp3_to_wav(data_path)
    #     except:
    #         print bird + ' error'
    #         pass
        # intro_text = GetIntro()
        # print intro_text
        # Intro(1, bird, intro_text, 'test').insert()
