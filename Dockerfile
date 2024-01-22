FROM python:3.11.5

RUN pip3 install poetry
RUN mkdir /data
RUN wget -q https://ai.stanford.edu/\~amaas/data/sentiment/aclImdb_v1.tar.gz -O - | tar -xz -C /data
COPY src /code/src
COPY pyproject.toml poetry.lock /code/
WORKDIR /code
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev
CMD ["poetry", "run", "python3", "-m", "src.main"]


