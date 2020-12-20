FROM python:3.7

COPY ./api ./requirements.txt /api/

WORKDIR api

RUN pip install uvicorn tortoise-orm[aiomysql] pydantic[email] \
    && pip install -r requirements.txt

CMD ["uvicorn", "api:app", "--reload"]
