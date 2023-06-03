FROM alpine
WORKDIR /app
RUN apk update && apk add python3 py3-pip ffmpeg
COPY ./entrypoint.sh .
RUN chmod +x entrypoint.sh
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY wav2mp3_api .
ENTRYPOINT ["sh","entrypoint.sh"]
