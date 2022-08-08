FROM ubuntu:20.04

WORKDIR /root

ENV DEBIAN_FRONTEND noninteractive
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo 'Asia/Shanghai' >/etc/timezone

RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt-get clean && \
    apt-get update -y && \
    apt-get install -y python3.8 python3-pip python3.8-dev git wget

RUN wget https://raw.iqiq.io/benx1n/wows-stats-bot/master/requirements.txt -O req1.txt && \
    wget https://raw.iqiq.io/Ice-Cirno/HoshinoBot/master/requirements.txt -O req2.txt && \
    python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip && \
    pip3 install -r req1.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip3 install -r req2.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip3 install markupsafe==2.0.1 -i https://pypi.tuna.tsinghua.edu.cn/simple


RUN git clone https://gitclone.com/github.com/Ice-Cirno/HoshinoBot.git /root/HoshinoBot&& \
    git clone https://gitclone.com/github.com/benx1n/wows-stats-bot.git /root/HoshinoBot/hoshino/modules/wows-stats-bot && \
    mv HoshinoBot/hoshino/config_example HoshinoBot/hoshino/config && \
    mkdir /root/config

COPY ./entrypoint.sh /root/entrypoint.sh

ENTRYPOINT [ "/bin/bash", "/root/entrypoint.sh" ]