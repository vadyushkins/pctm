FROM ubuntu:latest

COPY . /pctm

WORKDIR /pctm
RUN pip3 install -r requirements.txt