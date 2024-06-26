import hashlib
import os
from enum import Enum
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from application import dispatch
from dvadmin.utils.models import CoreModel, table_prefix, get_custom_app_models


class ProxiesActiveStatusChoice(Enum):
    NORMAL = '正常'
    ABNORMAL = '异常'


class ProxiesTypeChoice(Enum):
    VLESS = 'vless'
    SOCKS = 'socks5'


class Region(CoreModel):
    name = models.CharField(max_length=100, verbose_name="地域名称", help_text="地域名称")
    code = models.CharField(max_length=30, verbose_name="区域代码", help_text="区域代码")

    class Meta:
        db_table = table_prefix + "ucloud_region"
        verbose_name = "地域表"
        verbose_name_plural = verbose_name
        ordering = ("id",)


class VirtualNetwork(CoreModel):
    name = models.CharField(max_length=100, verbose_name="虚拟网卡名称", help_text="虚拟网卡名称")
    code = models.CharField(max_length=30, verbose_name="虚拟网卡id", help_text="虚拟网卡id")
    region = models.ForeignKey(to="Region", on_delete=models.SET_NULL, verbose_name="虚拟网卡地域",
                               help_text="虚拟网卡地域", null=True, blank=True)

    class Meta:
        db_table = table_prefix + "ucloud_virtual_network"
        verbose_name = "虚拟网卡表"
        verbose_name_plural = verbose_name
        ordering = ("id",)


class ShareBandwidth(CoreModel):
    name = models.CharField(max_length=100, verbose_name="共享带宽名称", help_text="共享带宽名称")
    code = models.CharField(max_length=30, verbose_name="共享带宽id", help_text="共享带宽id")
    region = models.ForeignKey(to="Region", on_delete=models.SET_NULL, verbose_name="共享带宽地域", help_text="共享带宽地域",
                               null=True, blank=True)

    class Meta:
        db_table = table_prefix + "ucloud_share_bandwidth"
        verbose_name = "共享带宽表"
        verbose_name_plural = verbose_name
        ordering = ("id",)


class PrivateIp(CoreModel):
    region = models.ForeignKey(to="Region", on_delete=models.SET_NULL, verbose_name="地域",
                               help_text="地域", null=True, blank=True)
    ip = models.CharField(max_length=30, verbose_name="内网ip", help_text="内网ip")
    eip = models.CharField(max_length=30, default=None, verbose_name="eip_ip", help_text="eip_ip", null=True, blank=True)
    eip_id = models.CharField(max_length=30, default=None, verbose_name="eip_id", help_text="eip_id", null=True, blank=True)
    private_ip_type = models.CharField(max_length=30, default=None, verbose_name="类型", help_text="类型")
    virtual_network_resource = models.ForeignKey(to="VirtualNetwork", on_delete=models.CASCADE, verbose_name="绑定资源",
                                                 help_text="绑定资源", null=True, blank=True)

    class Meta:
        db_table = table_prefix + "ucloud_private_ip"
        verbose_name = "内网ip表"
        verbose_name_plural = verbose_name
        ordering = ("id",)


class UHost(CoreModel):
    name = models.CharField(max_length=100, verbose_name="主机名称", help_text="主机名称")
    code = models.CharField(max_length=30, verbose_name="主机id", help_text="主机id")
    ip = models.CharField(max_length=30, verbose_name="主机ip", help_text="主机ip")
    region = models.ForeignKey(to="Region", on_delete=models.SET_NULL, verbose_name="主机地域", help_text="主机地域",
                               null=True, blank=True)
    share_bandwidth = models.ForeignKey(to="ShareBandwidth", on_delete=models.SET_NULL, verbose_name="共享带宽",
                                        help_text="共享带宽", null=True, blank=True)
    virtual_network = models.ForeignKey(to="VirtualNetwork", on_delete=models.SET_NULL, verbose_name="虚拟网卡",
                                        help_text="虚拟网卡", null=True, blank=True)

    class Meta:
        db_table = table_prefix + "ucloud_u_host"
        verbose_name = "主机表"
        verbose_name_plural = verbose_name
        ordering = ("id",)


class Proxies(CoreModel):
    private_ip = models.ForeignKey(to="PrivateIp", on_delete=models.SET_NULL, verbose_name="内网ip", help_text="内网ip",
                                   null=True, blank=True, default=None, related_name='proxies')
    eip = models.CharField(max_length=30, verbose_name="外网ip", help_text="外网ip")
    active_status = models.CharField(max_length=30,
                                     choices=[(tag.name, tag.value) for tag in ProxiesActiveStatusChoice],
                                     default=ProxiesActiveStatusChoice.NORMAL.name,
                                     verbose_name="存活状态",
                                     help_text="存活状态"
                                     )
    vless_port = models.IntegerField(verbose_name="vless端口", help_text="vless_端口", default=0)
    socks_port = models.IntegerField(verbose_name="socks端口", help_text="socks_端口", default=0)
    is_delete = models.BooleanField(verbose_name="是否删除", default=False)

    class Meta:
        db_table = table_prefix + "ucloud_proxies"
        verbose_name = "代理表"
        verbose_name_plural = verbose_name
        ordering = ("id",)
