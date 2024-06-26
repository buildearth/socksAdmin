# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework import serializers

from dvadmin.ucloud.models import UHost
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class UHostSerializer(CustomModelSerializer):
    class Meta:
        model = UHost
        fields = "__all__"
        read_only_fields = ["id"]


class UHostCreateUpdateSerializer(CustomModelSerializer):
    class Meta:
        model = UHost
        fields = '__all__'


class UHostViewSet(CustomModelViewSet):
    queryset = UHost.objects.all()
    serializer_class = UHostSerializer
    create_serializer_class = UHostCreateUpdateSerializer
    update_serializer_class = UHostCreateUpdateSerializer
    extra_filter_class = []

