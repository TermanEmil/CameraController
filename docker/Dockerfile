FROM python:3.6

COPY . /app
WORKDIR /app

RUN ./scripts/install_gphoto2.sh
RUN	./scripts/install_ykush.sh ||  echo 'Ykush failed to install. Ignoring' >&2

ENV PYTHONUNBUFFERED 1
RUN pip install -r requirements.txt
RUN python ./src/infrastructure/django_framework/manage.py migrate