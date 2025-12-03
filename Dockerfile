FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get install -y awscli build-essential libssl-dev libffi-dev python3-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

RUN apt-get update && pip install -r requirements.txt
CMD ["python3", "app.py"]
