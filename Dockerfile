FROM ubuntu:18.04

COPY . /pctm

WORKDIR /pctm
RUN pip3 install -r requirements.txt