FROM debian:bullseye-slim

#COPY pass /etc/mosquitto/
RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential default-libmysqlclient-dev \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY ./requirments.txt /app

RUN apt-get install libpq-dev python3-dev --assume-yes --force-yes

RUN apt-get install pkg-config python3-dev default-libmysqlclient-dev build-essential --assume-yes --force-yes

RUN pip install --no-cache-dir --requirement /app/requirments.txt

COPY . /app

EXPOSE 1883
EXPOSE 2020
EXPOSE 50050


CMD ["python","server.py"]
