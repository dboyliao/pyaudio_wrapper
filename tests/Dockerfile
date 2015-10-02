FROM ubuntu:14.04

# installing git and clone the code.
RUN apt-get install -y git && \
	git clone https://github.com/dboyliao/pyaudio_wrapper.git /root/pyaudio_wrapper && \
	cd /root/pyaudio_wrapper && \
	make install

CMD /bin/bash
