FROM python:3.11-alpine
LABEL authors="reflector"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]