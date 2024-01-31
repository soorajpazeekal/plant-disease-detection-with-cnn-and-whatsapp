# Use the official Python image as the base image with Python 3.8
FROM python:3.8


WORKDIR /app

COPY . /app

# Install necessary dependencies
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 5000

CMD ["python", "app.py"]
