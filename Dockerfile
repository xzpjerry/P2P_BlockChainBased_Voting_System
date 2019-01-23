FROM ubuntu:16.04
RUN apt update
RUN apt upgrade
EXPOSE 80 443
RUN mkdir /host