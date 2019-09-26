FROM python:3.7

RUN apt install git

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "address_manager.wsgi" ]
