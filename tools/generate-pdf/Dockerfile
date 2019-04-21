FROM ubuntu:bionic

RUN apt-get update -y
RUN apt-get install gnupg apt-transport-https ca-certificates software-properties-common -y
RUN add-apt-repository ppa:scribus/ppa
RUN apt-get update && apt-get install -y --allow-unauthenticated scribus-ng xvfb locales locales-all && rm -rf /var/lib/apt/lists/*

ADD scribus-launch.sh /app/
ADD generatepdf.py /app/

RUN mkdir /work
WORKDIR /app

# use with -v "$(pwd)":/work

ENTRYPOINT ["/app/scribus-launch.sh"]
