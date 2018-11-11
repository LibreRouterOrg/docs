FROM ubuntu:artful

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install gnupg apt-transport-https ca-certificates -y

RUN apt-get install python-software-properties software-properties-common -y
RUN add-apt-repository ppa:scribus/ppa
RUN apt-get update
RUN apt-get install -y --allow-unauthenticated scribus-ng locales locales-all
RUN rm -rf /var/lib/apt/lists/*

ADD scribus-launch.sh /scribus-launch.sh

CMD /scribus-launch.sh
