FROM --platform=linux/amd64  python:3.8.10-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update
RUN apt install wget gnupg gnupg1 gnupg2  curl  -y
RUN apt install -y unzip xvfb libxi6 libgconf-2-4  -y
RUN apt install default-jdk  -y
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py
COPY requirements.txt /root/requirements.txt
RUN pip3 install -r  /root/requirements.txt
RUN apt-get update

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update -qqy --no-install-recommends && apt-get install -qqy --no-install-recommends google-chrome-stable

COPY chromedriver /usr/local/bin/chromedriver
RUN chmod 755 /usr/local/bin/chromedriver
COPY xvfb-run-safe /usr/local/bin/xvfb-run-safe
RUN chmod 755 /usr/local/bin/xvfb-run-safe
COPY simplified_mlb.py /usr/local/bin/simplified_mlb.py
RUN chmod 075 /usr/local/bin/simplified_mlb.py
