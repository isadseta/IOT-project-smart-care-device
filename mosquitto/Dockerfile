##FROM ubuntu:22.04
##
##RUN apt-get update \
##    && apt-get install -y --no-install-recommends --no-install-suggests \
##    build-essential default-libmysqlclient-dev
###    && pip install --no-cache-dir --upgrade pip
##
##WORKDIR /app
##
##RUN apt-get install libpq-dev python3-dev --assume-yes --force-yes
##
##RUN apt-get install pkg-config python3-dev default-libmysqlclient-dev build-essential --assume-yes --force-yes
##
###RUN pip install --no-cache-dir --requirement /app/requirments.txt
##
##RUN apt-get update
##
##RUN apt-get -qq install software-properties-common
##
###RUN apt-get install add-apt-repository
##
##RUN apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
##
##RUN apt-get update
##
##RUN apt-get -qq install mosquitto
##
##RUN apt-get install mosquitto-clients
##
##RUN apt clean
##
###COPY ./requirments.txt /app
##
###COPY . /app
###
##
##EXPOSE 22
##
##EXPOSE 1883
##
##CMD "systemctl"
#FROM debian:bullseye-slim
#
## Install Mosquitto and required dependencies
#RUN apt-get update && apt-get install -y mosquitto
#RUN mkdir /mosquitto
#RUN mkdir /mosquitto/data
#
## Copy configuration file (if needed)
#COPY mosquitto.conf /etc/mosquitto/
#ENV MOSQUITTO_CONFIG /etc/mosquitto/mosquitto.conf
#
#COPY pass /etc/mosquitto/
#
## Expose the Mosquitto port (adjust as needed)
#EXPOSE 1883
#EXPOSE 1893
#
## Define the entrypoint for the container
#CMD ["mosquitto", "-v", "-c", "/etc/mosquitto/mosquitto.conf"]
# Use the official Eclipse Mosquitto image as the base image
FROM eclipse-mosquitto:latest

# Copy custom configuration files into the container
COPY mosquitto.conf /mosquitto/config/mosquitto.conf

# Expose MQTT default port and optional WebSocket port
EXPOSE 1883
EXPOSE 9001

# Optionally add persistence directory for message storage
VOLUME ["/mosquitto/data", "/mosquitto/log"]

# Run the Mosquitto broker
CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]