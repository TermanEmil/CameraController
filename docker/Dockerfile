FROM python:3.6

RUN	apt-get update && apt-get install -y \
	wget

RUN wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh -O /tmp/gphoto2-updater.sh \
&&  chmod +x /tmp/gphoto2-updater.sh \
&&  echo 2 | /tmp/gphoto2-updater.sh


ENV PYTHONUNBUFFERED 1
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN python ./src/infrastructure/django_framework/manage.py migrate