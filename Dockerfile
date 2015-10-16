FROM ubuntu:14.04

ADD . /root/pyaudio_wrapper

# installing git and clone the code.
RUN apt-get update && \
    apt-get install -y make build-essential python-dev python-pip && \
    cd /root/pyaudio_wrapper && make install

CMD /bin/bash
