# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework import serializers

from dvadmin.ucloud.models import VirtualNetwork
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class VirtualNetworkSerializer(CustomModelSerializer):
    """
    地域-序列化器
    """
    class Meta:
        model = VirtualNetwork
        fields = "__all__"
        read_only_fields = ["id"]


class VirtualNetworkCreateUpdateSerializer(CustomModelSerializer):
    """
    地区管理 创建/更新时的列化器
    """

    class Meta:
        model = VirtualNetwork
        fields = '__all__'


class VirtualNetworkViewSet(CustomModelViewSet):
    """
    地区管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = VirtualNetwork.objects.all()
    serializer_class = VirtualNetworkSerializer
    create_serializer_class = VirtualNetworkCreateUpdateSerializer
    update_serializer_class = VirtualNetworkCreateUpdateSerializer
    extra_filter_class = []

