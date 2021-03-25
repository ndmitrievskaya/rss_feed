FROM python:3.8

RUN mkdir /code

COPY requirements.txt /code

RUN pip install -r /code/requirements.txt

COPY . /code

WORKDIR /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

