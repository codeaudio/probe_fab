from django.contrib import admin

from api_notification.models import (
    MobileOperatorCode, Tag, MallingList, Message
)


@admin.register(MobileOperatorCode)
class MobileOperatorCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code',)
    search_fields = ('code',)
    list_filter = ('code',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(MallingList)
class MallingListAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'start_notification_date', 'end_notification_date', 'text'
    )
    search_fields = (
        'start_notification_date', 'end_notification_date', 'text'
    )
    list_filter = ('start_notification_date',)
    empty_value_display = '-пусто-'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'client')
    search_fields = ('status', 'phone_number', 'send_date')
    list_filter = ('malling_list', 'client')
    empty_value_display = '-пусто-'
