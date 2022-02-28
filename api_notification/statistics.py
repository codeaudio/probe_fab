from django.db.models import Count

from api_notification.models import MallingList


def generate_malling_statistics(obj: MallingList.objects):
    return {
        'malling_list': obj.prefetch_related(
            'messages'
        ).values(
            'start_notification_date',
            'end_notification_date',
            'messages__status',
            'id'
        ).annotate(count_messages=Count(
            'messages__status'
        ), client_count=Count('messages__client')),
        'detail': False
    }


def generate_malling_detail_statistics(obj: MallingList.objects):
    return {
        'malling_list': obj.prefetch_related(
            'messages__client'
        ).values(
            'start_notification_date',
            'end_notification_date',
            'messages__status',
            'messages__client',
            'messages__client__phone_number',
            'messages__client__mobile_operator_code__code',
            'messages__client__tag__name', 'id'
        ).annotate(count_messages=Count((
            'messages__status'
        ))),
        'detail': True
    }
