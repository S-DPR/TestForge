FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
  python3 python3-pip \
  default-jdk \
  g++ build-essential \
  curl unzip \
  && apt-get clean

RUN useradd -m runner
USER runner
WORKDIR /home/runner
