from django.urls import path
from rest_framework import routers

from dvadmin.ucloud.views.region import RegionViewSet

ucloud_url = routers.SimpleRouter()

ucloud_url.register(r'region', RegionViewSet)

urlpatterns = [
]
urlpatterns += ucloud_url.urls
