#coding=utf-8
import requests
import re
import os
from pydub import AudioSegment

def DownloadMP3(data_path):
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    rep = requests.get(url)
    htmls = re.findall(r'<a target="_blank" title="点击播放" href=\"(.*)\">第',rep.content)
    print htmls

    mp3 = []
    for i in htmls:
        rep1 = requests.get(i)
        mp3.append(re.findall(r'mp3:\"(.*)\"',rep1.content)[0])
    print mp3

    for u, i in zip(mp3,range(len(mp3))):
        with open(data_path+str(i)+'.mp3','wb+') as f:
            f.write(requests.get(u).content)
        print '[*] ' + str(i)
    return 0

def mp3_to_wav(data_path):
    for mp3file in [x for x in os.listdir(data_path) if x.endswith('.mp3')]:
        try:
            sound = AudioSegment.from_mp3(data_path+mp3file)
            sound.export(data_path+mp3file.split('.')[0]+'.wav', format="wav")
            os.remove(data_path + mp3file)
        except:
            print mp3file
            pass
    return 0

if __name__ == "__main__":

    data_path = u'/srv/flask/qiuqiuqiu/app/data/珍珠鸡/'
    url = 'http://sound.niaolei.org.cn/Numida-meleagris.html'

    #DownloadMP3(data_path)
    mp3_to_wav(data_path)
