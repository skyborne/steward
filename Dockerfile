FROM nginx:latest

MAINTAINER Skyborne <info@skyborne.co>

RUN mkdir /srv/steward
COPY src/* /srv/steward
RUN cd /srv/steward

RUN apt-get update

RUN apt-get install virtualenv
RUN apt-get install build-essential
RUN apt-get install python3-dev

RUN virtualenv .venv -p python3
RUN source .venv/bin/activate

RUN pip install -r config/requirements.txt
RUN pip install -v --no-binary :all: falcon

CMD ["gunicorn --workers=2 steward:api"]
