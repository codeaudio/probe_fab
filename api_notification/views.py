from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from logger import info_logger
from .filters import MallingListFilter
from .models import Tag, MobileOperatorCode, MallingList, Client, Message
from .pagination import CustomPagination
from .serializers import (UserSerializer, MobileOperatorCodeSerializer,
                          TagSerializer, MallingListSerializer,
                          MessageSerializer, MallingListCreateUpdateSerializer,
                          ClientSerializer)
from .statistics import (generate_malling_statistics,
                         generate_malling_detail_statistics)
from .utils import render_to_pdf


@method_decorator(info_logger, name='dispatch')
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    lookup_field = 'username'
    ordering_fields = ['id']


@method_decorator(info_logger, name='dispatch')
class MallingListViewSet(ModelViewSet):
    queryset = MallingList.objects.all()
    serializer_class = {
        'list': MallingListSerializer,
        'retrieve': MallingListSerializer,
        'destroy': MallingListSerializer,
        'create': MallingListCreateUpdateSerializer,
        'update': MallingListCreateUpdateSerializer,
        'partial_update': MallingListCreateUpdateSerializer
    }
    filterset_class = MallingListFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        return self.serializer_class.get(self.action)


@method_decorator(info_logger, name='dispatch')
class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = CustomPagination


@method_decorator(info_logger, name='dispatch')
class MobileOperatorCodeViewSet(ModelViewSet):
    queryset = MobileOperatorCode.objects.all()
    serializer_class = MobileOperatorCodeSerializer
    pagination_class = CustomPagination


@method_decorator(info_logger, name='dispatch')
class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = CustomPagination


@method_decorator(info_logger, name='dispatch')
class MessageListView(ListModelMixin, GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = CustomPagination


@method_decorator(info_logger, name='dispatch')
class StatisticView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    def list(self, request, *args, **kwargs):
        pdf = render_to_pdf(
            'statistic.html',
            generate_malling_statistics(MallingList.objects)
        )
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            return response
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        pdf = render_to_pdf(
            'statistic.html',
            generate_malling_detail_statistics(
                MallingList.objects.filter(id=pk)
            )
        )
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            return response
        return Response(status=status.HTTP_400_BAD_REQUEST)
