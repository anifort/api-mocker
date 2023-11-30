FROM python:3.10-slim

WORKDIR /backend

COPY ./ /backend

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
#RUN poetry config virtualenvs.create true
#RUN poetry config virtualenvs.in-project true

RUN poetry install

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]


