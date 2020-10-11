FROM ubuntu:18.04

COPY . /pctm

WORKDIR /pctm
RUN apt-get update && apt-get install -y \
    python3-pip
RUN pip3 install -r requirements.txt