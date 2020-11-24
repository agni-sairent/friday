FROM tiangolo/uvicorn-gunicorn-fastapi:latest

COPY . /app

WORKDIR /app

RUN pip install pipenv
RUN pipenv install

EXPOSE 8000
CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
