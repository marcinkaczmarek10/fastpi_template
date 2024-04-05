FROM python:3.11-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /fastapi_template

ENV TZ=Europe/Warsaw

COPY requitements_dev.txt requitements_dev.txt

RUN pip3 install --no-cache-dir --upgrade pip -r requitements_dev.txt

COPY ./entrypoint.sh .

COPY . .

ENTRYPOINT ["sh", "/fastapi_template/entrypoint.sh"]