FROM docker.io/nvidia/cuda:12.2.0-runtime-ubuntu22.04

RUN apt-get update
RUN apt-get --assume-yes install pip
RUN apt-get --assume-yes install python3
RUN alias python=/usr/bin/python3

WORKDIR /nlp_service
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ARG APP_DIR=/nlp_service
ENV PYTHONPATH "${PYTHONPATH}:${APP_DIR}"

COPY src/ ./src
COPY config.yaml .
COPY gradio_ui.py .

RUN ls -la

CMD ["python", "gradio_ui.py"]