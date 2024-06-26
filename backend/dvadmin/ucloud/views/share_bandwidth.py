# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework import serializers

from dvadmin.ucloud.models import ShareBandwidth
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class ShareBandwidthSerializer(CustomModelSerializer):
    class Meta:
        model = ShareBandwidth
        fields = "__all__"
        read_only_fields = ["id"]


class ShareBandwidthCreateUpdateSerializer(CustomModelSerializer):
    class Meta:
        model = ShareBandwidth
        fields = '__all__'


class ShareBandwidthViewSet(CustomModelViewSet):
    queryset = ShareBandwidth.objects.all()
    serializer_class = ShareBandwidthSerializer
    create_serializer_class = ShareBandwidthCreateUpdateSerializer
    update_serializer_class = ShareBandwidthCreateUpdateSerializer
    extra_filter_class = []

