FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    git

ENV DockerHOME=/code
WORKDIR $DockerHOME
RUN mkdir -p $DockerHOME
ADD ./requirements.txt /code/requirements.txt
ADD . $DockerHOME


RUN pip install --upgrade pip
# install dependencies
RUN pip install -r /code/requirements.txt
ENTRYPOINT ["bash","./docker-entrypoint.sh"]

EXPOSE 8000
