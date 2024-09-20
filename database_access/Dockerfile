FROM python:3.10-slim-bullseye

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

EXPOSE 50001

CMD ["python","server.py"]