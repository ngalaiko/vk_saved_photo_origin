FROM python:3.5.3

RUN apt-get update && \
    apt-get install -y \
    imagemagick

ADD . /root/vk_saved_photo_origin

WORKDIR /root/vk_saved_photo_origin

RUN pip3 install -r ./requirements.txt

RUN chmod +x start.sh
ENTRYPOINT ["./start.sh"]
