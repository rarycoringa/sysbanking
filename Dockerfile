FROM python:3.11-slim

RUN pip install pipenv

WORKDIR /app

COPY . /app

RUN pipenv install 
RUN pipenv run migrate

EXPOSE 8080

CMD ["pipenv", "run", "server", "0.0.0.0:8080"]