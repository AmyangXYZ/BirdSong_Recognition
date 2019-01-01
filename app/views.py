#coding=utf-8
import sys, os
from pydub import AudioSegment
from flask import render_template, url_for,request,redirect,session,flash,send_from_directory
from app import app
import time

sys.path.append('/home/amyang/Projects/BirdSong_Recognition/app/')

from sigproc import *

from sql import Query
from train import recognize

app.config['UPLOAD_FOLDER'] = '/home/amyang/Projects/BirdSong_Recognition/app/uploads/'
app.config['WaveForms_FOLDER'] = '/home/amyang/Projects/BirdSong_Recognition/app/waveforms/'
app.config['BirdsFiles_FOLDER'] = '/home/amyang/Projects/BirdSong_Recognition/app/birdsfiles/'
app.secret_key = os.urandom(24)


@app.route('/')
def welcome():
    return render_template('welcome.html', title="Welcome")

@app.route('/enjoy')
def enjoy():
    birds = Query.query_all()
    return render_template('enjoy.html',title='Enjoy',**locals())

@app.route('/bird/<birdname>')
def bird(birdname):
    bird = Query.query_bird_sciname(birdname)
    return render_template('bird.html',title=birdname,bird=bird)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/recognize', methods=['GET','POST'])
def Recognize():
    if request.method == 'POST':    # upload
        file = request.files['file']
        if file :
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
            t3 = '0.0000'

            # convert to wav
            if file.filename.split('.')[-1] != 'wav':
                bt3 = time.time()
                sound = AudioSegment.from_file(os.path.join(app.config['UPLOAD_FOLDER']+file.filename))
                os.remove(app.config['UPLOAD_FOLDER']+file.filename)
                file.filename = file.filename.replace(file.filename.split('.')[-1],'wav')
                sound.export(app.config['UPLOAD_FOLDER']+file.filename, format="wav")
                et3 = time.time()
                t3 = '%.4f'%(et3 - bt3)
            file_url = url_for('uploaded_file', filename=file.filename)
            audio_name = app.config['UPLOAD_FOLDER'] + file.filename
            bt0 = time.time()
            sig = SigProc(audio_name)
            et0 = time.time()
            t0 = '%.4f'%(et0 - bt0)
            bt1 = time.time()

            ## librosa will write a non-PCM16 .wav audio, which cannot displayed on html5, 
            ## so we have to drop the raw and output comparison function.

            # librosa.output.write_wav(app.config['UPLOAD_FOLDER'] + "output_" + file.filename, sig.logMMSE, sig.sr)
            # sound.export(app.config['UPLOAD_FOLDER']+"output_" +file.filename, format="mp3")
            img = PlotImg(sig.signal, sig.sr, sig.logMMSE, sig.MFCCs)
            et1 = time.time()
            t1 = '%.4f'%(et1 - bt1)
            bt2 = time.time()
            result = recognize(sig.MFCCs)
            et2 = time.time()
            t2 = '%.4f'%(et2 - bt2)
            wav_raw = 'Raw: <audio src="{}" controls="controls"></audio>'.format(file_url)
            # wav_output = 'Output: <audio src="{}" controls="controls"></audio>'.format("/uploads/output_"+file.filename+".mp3")
            bird = Query.query_bird_name(result)
            return render_template('recognize.html', title='Recognize',**locals())
    return render_template('recognize.html',title='Recognize')

@app.route('/waveforms/<filename>')
def waveforms(filename):
    return send_from_directory(app.config['WaveForms_FOLDER'],filename)

@app.route('/birdsfiles/<filename>')
def birdsfiles(filename):
    return send_from_directory(app.config['BirdsFiles_FOLDER'],filename)

