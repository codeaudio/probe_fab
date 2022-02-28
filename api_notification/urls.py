from django.urls import path, include
from .views import (StatisticView, UserViewSet,
                    MallingListViewSet, TagViewSet, MessageListView,
                    MobileOperatorCodeViewSet, ClientViewSet)

from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('clients', ClientViewSet, basename='clients')
router_v1.register('malling', MallingListViewSet, basename='malling')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('codes', MobileOperatorCodeViewSet, basename='codes')
router_v1.register('messages', MessageListView, basename='messages')
router_v1.register('statistic', StatisticView, basename='statistic')

urlpatterns = [
    path('', include(router_v1.urls)),
]
