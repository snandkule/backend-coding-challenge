FROM python:3.9

WORKDIR /gistapi

RUN pip install poetry
COPY pyproject.toml pyproject.toml
RUN poetry install

COPY . .

EXPOSE 5000

CMD ["poetry", "run", "flask", "--app=gistapi:app","run", "--host=0.0.0.0"]
