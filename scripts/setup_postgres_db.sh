DB_NAME='camera_controller_db';
DB_USER='camera_controller_user';

# Change the default password after setup
DB_PASSWORD='admin';
 
psql -U postgres -c "CREATE DATABASE ${DB_NAME}";
psql -U postgres -c "
CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';

ALTER ROLE ${DB_USER} SET client_encoding TO 'utf8';
ALTER ROLE ${DB_USER} SET default_transaction_isolation TO 'read committed';
ALTER ROLE ${DB_USER} SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
";
