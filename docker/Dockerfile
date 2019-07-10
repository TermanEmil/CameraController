FROM ubuntu:18.04
COPY . /app
WORKDIR /app

RUN ls -la

RUN	apt-get update && apt-get install -y \
	wget \
	g++ \
	gcc \
	software-properties-common


# python
RUN add-apt-repository ppa:deadsnakes/ppa -y \
&&	apt-get update && apt-get install -y \
	python3-pip


# gphoto2: install 2nd option (stable gphoto2)
RUN	wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh -O /tmp/gphoto2-updater.sh \
&&	chmod +x /tmp/gphoto2-updater.sh \
&&	echo 2 | /tmp/gphoto2-updater.sh

RUN ./configure

CMD sh ./run_server.sh