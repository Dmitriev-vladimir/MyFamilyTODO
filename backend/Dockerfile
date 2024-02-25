FROM python:3.11.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN apt-get update -y && apt-get upgrade -y

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system

COPY ./ ./

CMD ["uvicorn", "src/app:app", "--reload"]
