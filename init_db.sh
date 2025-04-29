#!/usr/bin/env bash

DIR="$PWD"

sudo yum update
sudo yum install -y postgresql-contrib postgresql-server

# Start PostgreSQL service
sudo postgresql-setup --initdb > /dev/null 2>&1
sudo systemctl start postgresql
sudo systemctl enable postgresql > /dev/null 2>&1

#configuring database
echo "Configuring database..."
PG_USER_DIR=$(echo ~postgres)
cd "$PG_USER_DIR" || exit

# Delete possible existing data
sudo -u postgres psql -c "DROP DATABASE IF EXISTS aid_db;" > /dev/null 2>&1
sudo -u postgres psql -c "DROP USER IF EXISTS python_client" > /dev/null 2>&1
sudo -u postgres psql -c "DROP USER IF EXISTS spring_client" > /dev/null 2>&1

# Changing Default Postgres User
echo "Please enter the password for the postgres root-user"
read -s postgres_password

sudo -u postgres psql -c "CREATE DATABASE aid_db;"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD '$postgres_password';" > /dev/null

# Creating the Python User
echo "Please enter the password for the python-user (will be exported to environment variables):"
read -s python_password

export PGPASSWORD="$python_password"
echo "export PGPASSWORD='$python_password'" >> ~/.bashrc
echo "export PGPASSWORD='$python_password'" >> ~/.bash_profile
echo "export PGPASSWORD='$python_password'" >> ~/.bash_login
echo "export PGPASSWORD='$python_password'" >> ~/.profile
source ~/.bashrc

sudo -u postgres psql -c "CREATE USER python_client PASSWORD '$PGPASSWORD';" > /dev/null
sudo -u postgres psql -c "ALTER ROLE python_client SET client_encoding TO 'utf8';" > /dev/null
sudo -u postgres psql -c "ALTER ROLE python_client SET default_transaction_isolation TO 'read committed';" > /dev/null
sudo -u postgres psql -c "ALTER ROLE python_client SET timezone TO 'Europe/Berlin';" > /dev/null
sudo -u postgres psql -c "GRANT CONNECT ON DATABASE aid_db TO python_client;" > /dev/null
sudo -u postgres psql -c "GRANT USAGE ON SCHEMA public TO python_client;" > /dev/null
sudo -u postgres psql -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO python_client;" > /dev/null

# Creating the Spring User
echo "Please enter the password for the spring-user (will be visible inside the application.properties):"
read -s spring_password

sudo -u postgres psql -c "CREATE USER spring_client PASSWORD '$spring_password';" > /dev/null
sudo -u postgres psql -c "ALTER ROLE spring_client SET client_encoding TO 'utf8';" > /dev/null
sudo -u postgres psql -c "ALTER ROLE spring_client SET default_transaction_isolation TO 'read committed';" > /dev/null
sudo -u postgres psql -c "ALTER ROLE spring_client SET timezone TO 'Europe/Berlin';" > /dev/null
sudo -u postgres psql -c "GRANT CONNECT ON DATABASE aid_db TO spring_client;" > /dev/null
sudo -u postgres psql -c "GRANT USAGE ON SCHEMA public TO spring_client;" > /dev/null
sudo -u postgres psql -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO spring_client;" > /dev/null

# Creating the Config Table
echo "Creating the config table..."
sudo -u postgres psql -d aid_db -c "CREATE TABLE IF NOT EXISTS config (id SERIAL PRIMARY KEY, app_name VARCHAR(255), activated BOOLEAN);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('7zip', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('adobe', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('adobe_enterprise', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('firefox_esr', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('gimp', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('inkscape', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('keepass', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('ms_powerbi_desktop', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('ms_powerbi_report_server', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('notepadpp', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('putty', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('sqldeveloper', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('sqlitebrowser', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('stunnel', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('sysinternal_utilities', TRUE);" > /dev/null
sudo -u postgres psql -d aid_db -c "INSERT INTO config (app_name, activated) VALUES ('winscp', TRUE);" > /dev/null

sudo -u postgres psql -d aid_db -c "GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE config TO spring_client;" > /dev/null
sudo -u postgres psql -d aid_db -c "GRANT SELECT ON TABLE config TO python_client;" > /dev/null



#TODO create the Tables and manage read and write access


