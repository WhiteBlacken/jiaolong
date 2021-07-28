from django.contrib import admin

# Register your models here.
from rbac.models import Group, User

admin.site.register(User)
admin.site.register(Group)