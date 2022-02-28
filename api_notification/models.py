from django.db import models
from django.db.models import CASCADE

from .models_validator import mobile_phone_validator


class MobileOperatorCode(models.Model):
    code = models.CharField(
        unique=True,
        max_length=50,
        verbose_name='Код оператора'
    )

    class Meta:
        db_table = 'mobile_operator_code'

    def __str__(self):
        return self.code


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        verbose_name='Тег'
    )

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name


class MallingList(models.Model):
    start_notification_date = models.DateTimeField(
        'Дата начала рассылки'
    )
    end_notification_date = models.DateTimeField(
        'Дата завершения рассылки'
    )
    text = models.CharField(max_length=500)

    class Meta:
        db_table = 'malling_list'


class Client(models.Model):
    phone_number = models.CharField(
        max_length=11,
        validators=[mobile_phone_validator]
    )
    mobile_operator_code = models.ForeignKey(
        MobileOperatorCode,
        related_name='client',
        verbose_name='Код оператора',
        on_delete=CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        related_name='client',
        verbose_name='Тег',
        on_delete=CASCADE
    )
    timezone = models.CharField(
        max_length=50
    )

    class Meta:
        db_table = 'client'


class Message(models.Model):
    STATUS_CHOICES = (
        ("SEND", "Send"),
        ("ERROR", "Error"),
        ("NEW", "New"),
    )
    send_date = models.DateTimeField(
        'Дата отправки',
        null=True
    )
    status = models.CharField(
        max_length=5,
        choices=STATUS_CHOICES
    )
    malling_list = models.ForeignKey(
        MallingList,
        related_name='messages',
        on_delete=CASCADE
    )
    client = models.ForeignKey(
        Client,
        related_name='messages',
        on_delete=CASCADE
    )

    class Meta:
        db_table = 'message'
