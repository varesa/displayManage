FROM registry.esav.fi/base/python3

MAINTAINER Esa Varemo <esa@kuivanto.fi>

EXPOSE 6543 22

# APPLICATION

ENV APP=displaymanage
ENV USER=$APP
ENV DIR=/$APP

RUN useradd $USER
RUN mkdir $DIR && chown $USER:$USER $DIR

USER $USER

RUN git clone https://github.com/varesa/displayManage.git $DIR
RUN git clone https://github.com/varesa/logviewer.git $DIR/app/static/logviewer

RUN mkdir $DIR/data
RUN mkdir $DIR/logs

WORKDIR /$DIR

USER root
RUN pip3.6 install --allow-external mysql-connector-python -e .
USER $USER

CMD ["pserve", "development.ini"]

VOLUME $DIR/data
VOLUME $DIR/logs
