FROM tiangolo/uwsgi-nginx-flask:python3.7
RUN pip install tqdm wheel pydub hmmlearn librosa sklearn matplotlib scipy
COPY ./app /app
