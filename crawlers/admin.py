from django.contrib import admin
from crawlers import models

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ['book_name', ]


class BookContentAdmin(admin.ModelAdmin):
    list_display = ['book_name_id', 'chapter']


admin.site.register(models.Book, BookAdmin)
admin.site.register(models.BookContent, BookContentAdmin)
