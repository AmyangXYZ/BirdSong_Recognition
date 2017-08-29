#coding=utf-8
import sys, os
from pydub import AudioSegment
from flask import render_template, url_for,request,redirect,session,flash,send_from_directory
from app import app
from sigproc import SigProc
sys.path.append('/srv/flask/BirdSong_Recognition/app/')
from sql import Query
from train import recognize


app.config['UPLOAD_FOLDER'] = '/srv/flask/BirdSong_Recognition/app/uploads/'
app.config['WaveForms_FOLDER'] = '/srv/flask/BirdSong_Recognition/app/waveforms/'
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

            # convert to wav
            if file.filename.split('.')[-1] != 'wav':
                sound = AudioSegment.from_file(os.path.join(app.config['UPLOAD_FOLDER']+file.filename))
                os.remove(app.config['UPLOAD_FOLDER']+file.filename)
                file.filename = file.filename.replace(file.filename.split('.')[-1],'wav')
                sound.export(app.config['UPLOAD_FOLDER']+file.filename, format="wav")

            file_url = url_for('uploaded_file', filename=file.filename)
            audio_name = app.config['UPLOAD_FOLDER'] + file.filename
            print audio_name
            sig = SigProc(audio_name)
            img = sig.PlotImg()
            result = unicode(recognize(audio_name), "utf-8")
            wav = '<audio src="{}" controls="controls"></audio>'.format(file_url)
            bird = Query.query_bird_name(result)
            return render_template('recognize.html', title='Recognize',**locals())
    return render_template('recognize.html',title='Recognize')

@app.route('/waveforms/<filename>')
def waveforms(filename):
    return send_from_directory(app.config['WaveForms_FOLDER'],filename)

