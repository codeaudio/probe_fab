import json
import os
from dataclasses import asdict
from datetime import datetime

import requests
from celery import shared_task
from django_celery_beat.models import PeriodicTask
from dotenv import load_dotenv

from .setup import setup
from api_notification.models import MallingList, Message
from api_notification.service.send_schema import Probe
from logger import log

load_dotenv()

setup()

TOKEN = os.environ.get('TOKEN')
TASK_SEND_URL = os.environ.get('TASK_SEND_URL')


@shared_task
def send(*args, **kwargs):
    all_sends = True
    malling_list_id, periodic_id = args
    malling_list_obj = MallingList.objects.prefetch_related(
        'messages'
    ).get(
        id=malling_list_id
    )
    messages = malling_list_obj.messages.filter(
        status__in=['New', 'Error']
    ).all()
    for element in messages:
        data = Probe(
            id=int(element.id),
            phone=int(element.client.phone_number),
            text=str(malling_list_obj.text)
        )
        try:
            headers = {"Authorization": f"Bearer {TOKEN}"}
            response = requests.post(
                f"{TASK_SEND_URL}{element.id}",
                headers=headers,
                data=json.dumps(asdict(data))
            )
            if response.ok:
                Message.objects.filter(
                    id=element.id
                ).update(
                    status='Send', send_date=datetime.now()
                )
            else:
                Message.objects.filter(id=element.id).update(status='Error')
                all_sends = False
        except Exception as e:
            Message.objects.filter(id=element.id).update(status='Error')
            all_sends = False
            log.error(e)
    if all_sends is True:
        PeriodicTask.objects.filter(id=periodic_id).delete()
