from django.db import models


# Create your models here.
class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=32)
    author = models.CharField(max_length=32)
    digest = models.TextField()
    current = models.IntegerField()
    read_count = models.IntegerField(default=0)  # 点击
    collect_count = models.IntegerField(default=0)  # 收藏
    using = models.BooleanField(default=False)  # 是否写入中


class BookContent(models.Model):
    book_name = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    chapter_count = models.IntegerField()  # 章节数
    chapter = models.CharField(max_length=64)
    content = models.TextField()
    collect_count = models.IntegerField(default=0)  # 收藏
    read_count = models.IntegerField(default=0)  # 点击
    update_time = models.DateTimeField()


class Comment(models.Model):
    book_id = models.IntegerField()
    chapter_count = models.IntegerField()
    user_name = models.CharField(max_length=20, default='匿名朋友')
    comment = models.TextField()
    ts = models.DateTimeField()
    agree = models.IntegerField(default=0)  # 点赞数
