# DialogueSearchSystem

Развёртывание NLP-сервиса:

* podman build -f Dockerfile -t nlp_service:v1
* podman run -d --device nvidia.com/gpu=all -v /home/aisummer/nlp_models:/nlp_service/models -v ./data:/nlp_service/data -p 7860:7860 --name nlp_service localhost/nlp_service:v1
* ssh -L 8080:localhost:7860 aisummer@172.20.6.160