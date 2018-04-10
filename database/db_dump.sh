#!/bin/bash
set -x
/etc/init.d/mysql start
/usr/bin/mysqld_safe > /dev/null 2>&1 &

echo "MYSQL_ROOT_USER=$MYSQL_ROOT_USER"
echo "MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD"

RET=1
while [[ RET -ne 0 ]]; do
    echo "=> Waiting for confirmation of MySQL service startup"
    sleep 10
    mysql -hdb -u$MYSQL_ROOT_USER -p$MYSQL_ROOT_PASSWORD -e "status" > /dev/null 2>&1
    RET=$?
done

RESULT=`mysql -hdb -u$MYSQL_ROOT_USER -p$MYSQL_ROOT_PASSWORD -e "SHOW DATABASES" | grep $MYSQL_DATABASE`

if [ "$RESULT" != "$MYSQL_DATABASE" ]; then
mysql -hdb -u$MYSQL_ROOT_USER -p$MYSQL_ROOT_PASSWORD < /docker-entrypoint-initdb.d/$MYSQL_DATABASE
fi