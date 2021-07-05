FROM python:3.8

RUN pip install cherrypy jinja2 pymssql

EXPOSE 3001

COPY ./ /app

WORKDIR "/app"
CMD ["python3.8", "serve.py"]

