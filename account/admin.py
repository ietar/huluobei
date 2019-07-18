from django.contrib import admin
from account.models import User
# Register your models here.


class Useradmin(admin.ModelAdmin):
    list_display = ['username', ]


admin.site.register(User, Useradmin)
