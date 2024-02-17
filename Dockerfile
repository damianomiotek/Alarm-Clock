# syntax=docker/dockerfile:1
FROM python:3.10
COPY . .
RUN apt-get update && apt-get install -y libx11-6 libxext-dev libxrender-dev libxinerama-dev libxi-dev libxrandr-dev \
libxcursor-dev libxcb-cursor0 libxtst-dev qt6-base-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["alarm_clock"]