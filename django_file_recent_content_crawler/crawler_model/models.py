# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class recent_content(models.Model):
    title=models.CharField(primary_key=True, max_length=254)
    Show_type=models.CharField(max_length=100, blank=True, null=True)
    Source=models.CharField(max_length=100, blank=True, null=True)
    Service=models.CharField(max_length=100, blank=True, null=True)
    content_type=models.CharField(max_length=100, blank=True, null=True)
    Added_to_site=models.CharField(max_length=200, blank=True, null=True)
    Updated_at_DB=models.CharField(max_length=200, blank=True, null=True)


    class Meta:
        ordering=["title"]


# @classmethod
# def truncate(cls):
#     with connection.cursor() as cursor:
#         cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))    
       