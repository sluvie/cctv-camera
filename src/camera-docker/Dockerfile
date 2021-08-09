FROM python:3.8

RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev

RUN pip install flask jinja2 psycopg2-binary opencv-python requests bs4

EXPOSE 3002

COPY ./ /app

WORKDIR "/app"
CMD ["python3.8", "server.py"]

