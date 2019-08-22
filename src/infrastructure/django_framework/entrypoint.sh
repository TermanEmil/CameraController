#!/bin/bash

python manage.py migrate;
python manage.py loaddata fav_field_initial || echo 'Failed to load initial data. Ignoring ---';
(cat ./web/create_default_superuser.sh | python manage.py shell 2>&-) || echo 'Failed to create superuser. Ignoring ---';