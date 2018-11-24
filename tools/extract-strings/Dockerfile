FROM python:alpine3.7
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN mkdir /app
ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt

ADD extract-strings.py /app/
RUN mkdir /work
WORKDIR /app
ENTRYPOINT  ["python", "./extract-strings.py"]
