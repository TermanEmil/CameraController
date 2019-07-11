FROM python:3.6

RUN	apt-get update && apt-get install -y \
	gphoto2=2.5.11-1 \
    libgphoto2-dev=2.5.12-1


ENV PYTHONUNBUFFERED 1
COPY . /app
WORKDIR /app

RUN ./configure