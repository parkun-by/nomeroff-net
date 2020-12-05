FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN apt-get update && apt-get install -y gcc libglib2.0 libsm6 libfontconfig1 libxrender1 libxtst6 liblzma-dev libgl1-mesa-glx git
RUN git clone https://github.com/youngwanLEE/centermask2.git /app/centermask2

COPY . /app
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
RUN pip install 'git+https://github.com/facebookresearch/detectron2.git'
