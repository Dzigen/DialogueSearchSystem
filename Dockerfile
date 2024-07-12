FROM docker.io/nvidia/cuda:12.2.0-runtime-ubuntu22.04

RUN apt-get update
RUN apt-get --assume-yes install pip
RUN apt-get --assume-yes install python3
RUN alias python=/usr/bin/python3

WORKDIR /nlp_service
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get -y install uvicorn
RUN pip install fastapi

ARG APP_DIR=/nlp_service
ENV PYTHONPATH "${PYTHONPATH}:${APP_DIR}"

COPY src/ ./src
COPY config.yaml .

RUN ls -la

CMD ["uvicorn", "src.api:app", "--reload", "--host", "0.0.0.0", "--port", "8008"]