from django.http import HttpResponse
from crawlers.models import Book, BookContent
from crawlers import biqooge
from django.utils import timezone
# Create your views here.


def get_chapter(request):
    # 获取简介
    try:
        book_id = request.GET['id']
    except KeyError:
        book_id = 1
    # ids = Book.objects.all()
    # print(len(ids))
    qset = Book.objects.filter(book_id=book_id)
    if len(qset) != 0:
        # 已有
        # current_chapter = qset[0].current
        return HttpResponse(f'有了 《{qset[0].book_name}》')
    else:
        current_chapter = 1
        try:
            name, author, digest = biqooge.get_a_chapter(book_id=book_id)
        except IndexError:
            return HttpResponse('该书不存在')
        new_book = Book.objects.create(
            book_id=book_id, book_name=name, author=author, digest=digest, current=current_chapter)
        new_book.save()

    return HttpResponse(f'{name, author, digest}')


def get_content(request):
    # 爬内容了
    try:
        book_id = request.GET['id']
    except KeyError:
        book_id = 1

    try:
        target = int(request.GET['target'])
    except KeyError:
        target = 1
    except ValueError:
        return HttpResponse('target(爬取章节数)必须为整数')

    # print(f'book_id, count {book_id, target}')
    qset = Book.objects.filter(book_id=book_id)
    if len(qset) != 0:
        # 已有
        book = qset[0]
        current_chapter = qset[0].current
    else:
        # current_chapter = 1
        return HttpResponse('还没这本书的简介 先去get_chapter')

    chapters = biqooge.get_chapters(
        book_id=book_id, current_chapter=current_chapter, chapter_count=target)
    count = 0
    r = ''
    for chapter in chapters:
        chapter_name = chapter.a.text.strip()
        url1 = chapter.a['href']
        url = biqooge.root_url + url1
        content = biqooge.get_content(content_url=url)
        new_content = BookContent.objects.create(
            book_name=book,
            chapter_count=book.current,
            chapter=chapter_name,
            content=content,
            update_time=timezone.now()
        )
        new_content.save()
        count += 1
        book.current = book.current + 1
        book.save()
        r = f'已爬取 {count} 章,当前待爬取章节数为 {book.current}'
        print(r)
    return HttpResponse(r)
