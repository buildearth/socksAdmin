# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework import serializers
from rest_framework.decorators import action

from dvadmin.ucloud.models import PrivateIp, Proxies, ProxiesActiveStatusChoice
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class PrivateIpSerializer(CustomModelSerializer):
    class Meta:
        model = PrivateIp
        fields = "__all__"
        read_only_fields = ["id"]


class PrivateIpCreateUpdateSerializer(CustomModelSerializer):
    class Meta:
        model = PrivateIp
        fields = '__all__'


class PrivateIpViewSet(CustomModelViewSet):
    queryset = PrivateIp.objects.all()
    serializer_class = PrivateIpSerializer
    create_serializer_class = PrivateIpCreateUpdateSerializer
    update_serializer_class = PrivateIpCreateUpdateSerializer
    extra_filter_class = []

    @action(methods=["POST"],  detail=True)
    def bind_eip(self, request, pk=None):
        """
        生成eip，然后
        绑定eip
        """
        ...

    @action(methods=["POST"], detail=True)
    def release_eip(self, request, pk=None):
        """
        释放eip，将proxies表中原来的置为空
        """

        obj = PrivateIp.objects.filter(id=pk).first()
        if not obj:
            return ErrorResponse(msg="{} 不存在".format(pk))
        # 释放eip

        proxy_obj = Proxies.objects.filter(private_ip=obj, eip=obj.eip).first()
        if not proxy_obj:
            return ErrorResponse(msg="{} 不存在".format(obj.eip))
        # 将代理表中的内网ip去掉
        proxy_obj.active_status = ProxiesActiveStatusChoice.ABNORMAL.name
        proxy_obj.private_ip = None
        proxy_obj.save()

        obj.eip = ""
        obj.eip_id = ""
        obj.save()
        return SuccessResponse(msg="{} 已解绑".format(obj.ip))





