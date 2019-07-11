FROM python:3.6

RUN	apt-get update && apt-get install -y \
	gphoto2=2.5.11-1 \
    libgphoto2-dev=2.5.12-1

RUN wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh -O /tmp/gphoto2-updater.sh \
&&  chmod +x /tmp/gphoto2-updater.sh \
&&  echo 2 | /tmp/gphoto2-updater.sh


ENV PYTHONUNBUFFERED 1
COPY . /app
WORKDIR /app

RUN ./configure