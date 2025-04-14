#!/usr/bin/env bash

DIR="$PWD"

sudo yum update
sudo yum install -y postgresql postgresql-contrib nano

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Set Timezone in Linux (for Cron)
echo "Setting timezone..."
sudo timedatectl set-timezone Europe/Berlin

#configuring database
echo "Configuring database..."
PG_USER_DIR=$(echo ~postgres)
cd "$PG_USER_DIR" || exit

#set postgres password
echo "Please enter the password for the postgres root-user"
read -s postgres_password

sudo -u postgres psql -c "CREATE DATABASE aid_db;"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD '$postgres_password';"
#!/usr/bin/env bash

DIR="$PWD"

sudo yum update
sudo yum install -y postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Set Timezone in Linux (for Cron)
echo "Setting timezone..."
sudo timedatectl set-timezone Europe/Berlin

#configuring database
echo "Configuring database..."
PG_USER_DIR=$(echo ~postgres)
cd "$PG_USER_DIR" || exit

# Changing Default Postgres User
echo "Please enter the password for the postgres root-user"
read -s postgres_password

sudo -u postgres psql -c "CREATE DATABASE aid_db;"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD '$postgres_password';"

# Creating the Python User
echo "Please enter the password for the python-user (will be exported to environment variables):"
read -s python_password

export PGPASSWORD="$python_password"
echo "export PGPASSWORD='$python_password'" >> ~/.bashrc
source ~/.bashrc

sudo -u postgres psql -c "CREATE USER python_client PASSWORD '$PGPASSWORD';"
sudo -u postgres psql -c "ALTER ROLE python_client SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE python_client SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE python_client SET timezone TO 'Europe/Berlin';"
sudo -u postgres psql -c "GRANT CONNECT ON DATABASE scraper_db TO python_client;"
sudo -u postgres psql -c "GRANT USAGE ON SCHEMA public TO python_client;"
sudo -u postgres psql -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO python_client;"

# Creating the Spring User
echo "Please enter the password for the spring-user (will be visible inside the application properties):"
read -s spring_password

sudo -u postgres psql -c "CREATE USER spring_client PASSWORD '$spring_password';"
sudo -u postgres psql -c "ALTER ROLE spring_client SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE spring_client SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE spring_client SET timezone TO 'Europe/Berlin';"
sudo -u postgres psql -c "GRANT CONNECT ON DATABASE scraper_db TO spring_client;"
sudo -u postgres psql -c "GRANT USAGE ON SCHEMA public TO spring_client;"
sudo -u postgres psql -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO spring_client;"

#TODO create the Tables and manage read and write access


