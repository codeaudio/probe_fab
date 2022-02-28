import json
from datetime import datetime

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from api_notification.models import MallingList
from probe_fab.tasks import send


def create_task(pk):
    instance = MallingList.objects.filter(
        id=pk, messages__status='New'
    ).prefetch_related(
        'messages__client'
    ).first()
    now_date = datetime.now().timestamp()
    instance_date = instance.start_notification_date.timestamp()
    if now_date == instance_date:
        send(instance)
    elif now_date < instance_date:
        now = instance.start_notification_date
        expires = instance.end_notification_date
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS
        )
        periodic_task = PeriodicTask(
            interval=schedule,  # we created this above.
            start_time=now,
            name=f"{instance}",
            task='probe_fab.tasks.send',
            expires=expires
        )
        periodic_task.save()
        periodic_task.args = json.dumps([pk, periodic_task.id])
        periodic_task.save()
