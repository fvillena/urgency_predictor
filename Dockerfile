FROM alpine

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

# install chromedriver

RUN apk update
RUN apk add build-base python3 python3-dev py3-pip py3-pandas
RUN apk add chromium chromium-chromedriver
RUN apk add xvfb
RUN apk add bash
RUN apk add xdpyinfo

# upgrade pip
RUN python3 -m pip install --upgrade pip

# install selenium
RUN python3 -m pip install selenium

RUN python3 -m pip install ipython

RUN python3 -m pip install PyVirtualDisplay

RUN python3 -m pip install xlrd