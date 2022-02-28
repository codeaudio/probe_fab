Клонируйте репо git clone ...
создаеть env c перменными
```
TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzcyMzM5MzEsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IkpvaG5Ib3JzZUNvaW4ifQ.0Ah6cEGl-dw0zYi15uBrx9eaYGXSRTWXgOVtzfRhREE
TASK_SEND_URL=https://probe.fbrq.cloud/v1/send/
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=django-insecure-b)xxb9&&*rp!qmjd3+9m9=y-9cm^n)=f9-#w(eadmdxwcbd2a0
DB=postgresql
```
создать и запустить контейнеры docker-compose up --build (3 контейнера прилоежние, postgres, nginx)
перейти в контейнер и запустить celery
docker exec -it <id контейнера> bash
```
celery -A probe_fab worker --loglevel=INFO --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo
celery -A probe_fab.celery  beat -l info -S django
```
CELERY_BROKER_URL = 'amqp://guest:guest@localhost' локлаьно
из контейнера CELERY_BROKER_URL = 'amqp://guest:guest@bvz имя контейнера'