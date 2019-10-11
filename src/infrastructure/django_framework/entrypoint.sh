#!/bin/bash

python manage.py migrate;
python manage.py loaddata camera_config_fixtures || echo 'Failed to load initial data. Ignoring ---';
(cat ./web/create_default_superuser.sh | python manage.py shell 2>&-) || echo 'Failed to create superuser. Ignoring ---';