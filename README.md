# speech-webui
this is a webui for the openai audio speech endpoint, as served by https://github.com/matatonic/openedai-speech


# usage
## docker registry 
pull the latest image
´´´ dockcer pull ghcr.io/mreitschuster/speech-webui:latest ´´´


## docker local build
- git clone this repo
- adjsut the env variables in docker-compose.yaml
- docker compose up


## run app.py
git clone the repo
run with
´´´ SERVER_URL="http://localhost:11435/v1/audio/speech" VOICES="alloy,echo,fable,onyx,nova,shimmer" MODELS="tts-1-hd,tts-1" python app.py ´´´