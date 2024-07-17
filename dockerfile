FROM python:3.11-alpine

WORKDIR /aiohttp_app
EXPOSE 8080

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT python main.py