FROM python:3.6.2-slim
MAINTAINER Lorena Barreto <lorenasimedo@gmail.com>

RUN apt-get update && apt-get install -qq -y \
  build-essential --no-install-recommends

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app

RUN pip install -r requirements.txt

ADD . /app

CMD ["python", "run.py"]
