# A MySQL container.
FROM mysql:5.7
LABEL maintainer="Ramendra Pratap Singh"
ADD phone_dir.sql /docker-entrypoint-initdb.d
ADD db_dump.sh /

EXPOSE 3306
CMD ["mysqld"]
