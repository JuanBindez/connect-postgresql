

# DataBase

#### install postgresql on linux
     sudo apt update
     sudo apt install postgresql postgresql-contrib

#### install flask and psycopg2 connector
     pip install Flask psycopg2-binary

#### access postgres
    sudo -i -u postgres
    psql

### executar commands
    CREATE USER myuser WITH PASSWORD 'mypassword';
    ALTER USER myuser WITH SUPERUSER;
    CREATE DATABASE mydatabase;
    GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
    \q

### list databases
    \l

### databse access
    c\ mydatabase

### verify useruser
    sudo -i -u postgres
    psql
    \dn+

### exit of the shell from postgreSQL
    \q
    exit