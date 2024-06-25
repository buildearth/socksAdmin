import hashlib
import os

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from application import dispatch
from dvadmin.utils.models import CoreModel, table_prefix, get_custom_app_models


class Region(CoreModel):
    name = models.CharField(max_length=100, verbose_name="地域名称", help_text="地域名称")
    code = models.CharField(max_length=30, verbose_name="区域代码", help_text="区域代码")

    class Meta:
        db_table = table_prefix + "ucloud_region"
        verbose_name = "地域表"
        verbose_name_plural = verbose_name
        ordering = ("id",)

