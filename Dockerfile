FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN apt-get update -y
RUN apt-get install python3-tk -y
EXPOSE 8080
CMD ["python3", "/app/Gestionnaire de ressources3.py"]
