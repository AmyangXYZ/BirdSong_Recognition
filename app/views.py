import sys, os

from flask import render_template, url_for,request,redirect,session,flash,send_from_directory
from app import app
from sigproc import SigProc
sys.path.append('/srv/flask/BirdSong_Recognition/app/')

from train import predict


app.config['UPLOAD_FOLDER'] = '/srv/flask/BirdSong_Recognition/app/uploads/'
app.config['WaveForms_FOLDER'] = '/srv/flask/BirdSong_Recognition/app/waveforms/'
app.secret_key = os.urandom(24)

@app.route('/')
def welcome():
    return render_template('welcome.html', title="Welcome")

@app.route('/enjoy')
def enjoy():
    return render_template('enjoy.html',title='Enjoy')

@app.route('/about')
def about():
    return render_template('about.html',title='Enjoy')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/recognize', methods=['GET','POST'])
def recognize():
    if request.method == 'POST':    # upload
        file = request.files['file']
        if file :
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
            file_url = url_for('uploaded_file', filename=file.filename)
            audio_name = app.config['UPLOAD_FOLDER'] + file.filename
            sig = SigProc(audio_name)
            img = sig.PlotImg()
            result = unicode(predict(audio_name), "utf-8")
            wav = '<audio src="{}" controls="controls"></audio>'.format(file_url)
            return render_template('recognize.html', title='Recognize',**locals())
    return render_template('recognize.html',title='recognize')

@app.route('/waveforms/<filename>')
def waveforms(filename):
    return send_from_directory(app.config['WaveForms_FOLDER'],filename)

