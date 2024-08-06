#!/bin/sh
service mysql start;

# Reset MySQL pwd
/usr/bin/mysqladmin

rm -rf file.json;

sleep 1;

echo "DROP USER IF EXISTS 'hbnb_test'@'localhost';" | sudo mysql;
echo "DROP DATABASE IF EXISTS hbnb_test_db;" | sudo mysql;

sleep 1;

echo "CREATE DATABASE IF NOT EXISTS hbnb_test_db;" | sudo  mysql;
echo "CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost';" | sudo  mysql;
echo "SET PASSWORD FOR 'hbnb_test'@'localhost' = 'hbnb_test_pwd';" | sudo mysql;
echo "GRANT ALL ON hbnb_test_db.* TO 'hbnb_test'@'localhost';" | sudo mysql;
echo "GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';" | sudo mysql;
echo "FLUSH PRIVILEGES;" | sudo  mysql;

