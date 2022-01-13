# -*- coding: utf-8 -*-
from asgiref.sync import sync_to_async
from django.utils import timezone

from crawlers import biqooge
from crawlers.models import Book, BookContent
from utils.any import logger


@sync_to_async
def async_get_content(book_id, current_chapter, target, prefix):
    book1 = Book.objects.get(book_id=book_id)
    chapters = biqooge.get_chapters(
        book_id=book_id, current_chapter=current_chapter, chapter_count=target, prefix=prefix)
    count = 0

    for chapter in chapters:
        chapter_name = chapter.a.text.strip()
        url1 = chapter.a['href']
        url = biqooge.root_url + url1
        content = biqooge.get_content(content_url=url)
        # content = sync_to_async(biqooge.get_content)(content_url=url)
        new_content = BookContent.objects.create(
            book_name=book1,
            chapter_count=book1.current,
            chapter=chapter_name,
            content=content,
            update_time=timezone.now()
        )
        new_content.save()
        count += 1
        book1.current = book1.current + 1
        book1.save()

    book1.using = False
    book1.save()
    return book1.current
