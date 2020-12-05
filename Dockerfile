FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN apt-get update && apt-get install -y \
    gcc \
    libglib2.0 \
    libsm6 \
    libfontconfig1 \
    libxrender1 \
    libxtst6 \
    liblzma-dev \
    libgl1-mesa-glx \
    libturbojpeg0 \
    git

COPY . /app

RUN pip install --upgrade pip \
    && pip install "torch>=1.8" \
    && pip install "PyYAML>=5.4" \
    && pip install "torchvision>=0.9" \
    && pip install Cython \
    && pip install numpy \
    && pip install -r /app/requirements.txt
