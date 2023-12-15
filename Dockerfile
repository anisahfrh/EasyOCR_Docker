FROM nvidia/cuda:11.8.0-base-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
ARG service_home="/home/ubuntu/"

RUN apt-get update -y && \
    apt-get install -y \
		python3-pip python3.8-dev python3.8-distutils python3.8-venv \
		libglib2.0-0

RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/li

WORKDIR /home/ubuntu/

RUN alias pip=pip3
RUN python3 -m pip install --upgrade pip
RUN python3 --version
RUN pip install torch torchvision torchaudio -f https://download.pytorch.org/whl/cu111/torch_stable.html

ADD ./main.py /home/ubuntu/
ADD ./requirements.txt /home/ubuntu/
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["/home/ubuntu/main.py"]
