from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    # 权限设置的简单点
    group = models.ForeignKey('Group', on_delete=models.CASCADE,default=2)

    def __str__(self):
        return self.username


class Group(models.Model):
    group_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.group_name
