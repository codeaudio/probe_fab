FROM python:3.9
WORKDIR /probe
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
RUN apt-get -y update && apt-get install -y nano
RUN python manage.py collectstatic --noinput