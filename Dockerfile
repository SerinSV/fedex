FROM python:3.8
#RUN apt-get update && apt-get install tzdata openssl -y
#RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008"]
