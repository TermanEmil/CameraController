FROM python:3.6

COPY . /app
WORKDIR /app

RUN ./scripts/install_gphoto2.sh
RUN	./scripts/install_ykush.sh ||  echo 'Ykush failed to install. Ignoring' >&2

ENV PYTHONUNBUFFERED 1
RUN pip install -r requirements.txt
RUN python ./src/infrastructure/django_framework/manage.py migrate

# Load initial Fav fields
RUN python ./src/infrastructure/django_framework/manage.py loaddata fav_field_initial

# Create default superuser
RUN cat web/create_default_superuser.sh | python ./src/infrastructure/django_framework/manage.py shell

# Migrate again coz of some shit.
RUN python ./src/infrastructure/django_framework/manage.py migrate