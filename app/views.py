#coding=utf-8
from flask import render_template, url_for,request,redirect,session,flash,send_from_directory
from app import app
from analyse import analyse
import os

app.config['UPLOAD_FOLDER'] = '/srv/flask/qiuqiuqiu/app/uploads/'
app.config['WaveForms_FOLDER'] = '/srv/flask/qiuqiuqiu/app/waveforms/'

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

@app.route('/identify', methods=['GET','POST'])
def identify():
    if request.method == 'POST':    # upload
        file = request.files['file']
        if file :
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
            file_url = url_for('uploaded_file', filename=file.filename)
            audio = app.config['UPLOAD_FOLDER'] + file.filename

            anal = analyse(audio)
            img = anal.getImg()
            wav = '<audio src="{}" controls="controls"></audio>'.format(file_url)
            return render_template('identify.html', title='Identify',**locals())
    return render_template('identify.html',title='Identify')

@app.route('/waveforms/<filename>')
def waveforms(filename):
    return send_from_directory(app.config['WaveForms_FOLDER'],filename)