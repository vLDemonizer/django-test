FROM ubuntu:16.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get update --fix-missing && \
    apt-get install -y \
        apt-utils \
        bash-completion \
        git \
        curl \
        python3-dev \
        python3-pip \
        python3-software-properties \
        supervisor \
        vim 

ADD ./requirements.txt /tmp/

RUN pip3 install --timeout 1000 --upgrade pip

RUN pip3 install --timeout 1000 -r /tmp/requirements.txt

RUN service supervisor stop

ADD docker/supervisor.conf /etc/supervisor/conf.d/visualize.conf

ADD docker/start.sh /root/

RUN chmod 700 /root/start.sh

WORKDIR /root/visualize

EXPOSE 8000

CMD ["/root/start.sh"]