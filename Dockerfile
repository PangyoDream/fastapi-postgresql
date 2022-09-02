FROM python:3.8

RUN pip install poetry

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN poetry install

COPY . /code/

CMD ["poetry", "run", "uvicorn", "main:app"]