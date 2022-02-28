from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_notification.models import (
    MobileOperatorCode, Tag, MallingList, Message, Client
)
from api_notification.service.create_task import create_task


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user: User = super().validate(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class MobileOperatorCodeSerializer(ModelSerializer):
    class Meta:
        model = MobileOperatorCode
        fields = '__all__'


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class MallingListSerializer(ModelSerializer):
    class Meta:
        model = MallingList
        fields = '__all__'


class MallingListCreateUpdateSerializer(ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField())
    codes = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = MallingList
        fields = '__all__'

    def validate(self, data):
        tags = data.get('tags')
        codes = data.get('codes')
        if len(tags) == 0 or len(codes) == 0:
            raise serializers.ValidationError(
                f"tags {tags} or codes {codes} cant be empty"
            )
        tags_qs = Tag.objects.filter(name__in=tags)
        codes_qs = MobileOperatorCode.objects.filter(
            code__in=codes
        )
        if tags_qs.count() != len(tags):
            raise serializers.ValidationError(
                f"tags exists {tags_qs.values_list('name')}"
            )
        if codes_qs.count() != len(codes):
            raise serializers.ValidationError(
                f"codes exists {codes_qs.values_list('code')}"
            )
        return data

    def create(self, validated_data):
        client = Client.objects.filter(
            tag__name__in=validated_data.get('tags'),
            mobile_operator_code__code__in=validated_data.get('codes')
        )
        if not client:
            return serializers.ValidationError(client)
        malling_list_instance = MallingList.objects.create(
            start_notification_date=validated_data.get(
                'start_notification_date'
            ),
            end_notification_date=validated_data.get('end_notification_date'),
            text=validated_data.get('text'),
        )
        for clint_obj in client:
            Message.objects.create(
                send_date=None,
                status='New',
                malling_list=malling_list_instance,
                client=clint_obj
            )

        create_task(malling_list_instance.id)
        return malling_list_instance

    def update(self, instance, validated_data):
        client = Client.objects.filter(
            tag__name__in=validated_data.get('tags'),
            mobile_operator_code__code__in=validated_data.get('codes')
        )
        if client.exists():
            instance(
                start_notification_date=validated_data.get(
                    'start_notification_date'
                ),
                end_notification_date=validated_data.get(
                    'end_notification_date'
                ),
                text=validated_data.get('text'),
            ).save()
            for clint_obj in client:
                Message.objects.create(
                    send_date=None,
                    status='New',
                    malling_list=instance,
                    client=clint_obj
                )
            return instance

    def to_representation(self, instance):
        start_notification_date = self.fields['start_notification_date']
        start_notif_date_value = start_notification_date.to_representation(
            start_notification_date.get_attribute(instance)
        )
        end_notification_date = self.fields['end_notification_date']
        end_notif_date_value = end_notification_date.to_representation(
            end_notification_date.get_attribute(instance)
        )
        text = self.fields['text']
        text_value = text.to_representation(
            text.get_attribute(instance)
        )
        return {
            'start_notification_date': start_notif_date_value,
            'end_notification_date': end_notif_date_value,
            'text': text_value,
        }


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
