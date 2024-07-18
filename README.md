# DialogueSearchSystem

Развёртывание NLP-сервиса:

* podman build -f Dockerfile -t nlp_service:v1
* podman run -d --device nvidia.com/gpu=all -v /home/aisummer/mikhail_workspace/gradio_cached_examples:/nlp_service/gradio_cached_examples -v /home/aisummer/nlp_models:/nlp_service/models -v ./data:/nlp_service/data -p 9090:9090 --name nlp_service localhost/nlp_service:v1
* ssh -L 8080:localhost:9090 aisummer@172.20.6.160
