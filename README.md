# DialogueSearchSystem

Развёртывание NLP-сервиса:

* podman network create nlp_network
* podman run -d --device nvidia.com/gpu=all -h llama_host --network nlp_network -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
* podman build -f Dockerfile -t nlp_service:v1
* podman run -d --device nvidia.com/gpu=all -h nlpservice_host --network nlp_network -v ./models:/nlp_service/models -v ./data:/nlp_service/data -p 8008:8008 --name nlp_service localhost/nlp_service:v1