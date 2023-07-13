FROM python:3.11

WORKDIR /bot

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY main .

CMD [ "python", "main.py" ]