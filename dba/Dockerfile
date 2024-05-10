FROM postgres:9.6.24-alpine
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD crazydata
ENV POSTGRES_DB framecolector
ADD ./schema/framecolector.sql /docker-entrypoint-initdb.d/
