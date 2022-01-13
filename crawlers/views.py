# import logging
import logging
import time
# from threading import Lock
import traceback

from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render

from account.models import User
from crawlers.models import Book, BookContent, Comment
from crawlers import biqooge
from django.utils import timezone
import typing
import json
# Create your views here.


ret_u = typing.TypeVar('ret_u', bool, User)
logger = logging.getLogger('django')


def login_check(request) -> ret_u:
    try:
        user = request.session['user']
    except KeyError:
        # 没这个键
        return False
    u = User.objects.filter(username__exact=user['username'])
    if len(u) == 1:
        u = u[0]
    else:
        # 查不着
        request.session.clear()
        return False

    return u


def get_chapter(request):
    # 获取简介 自用
    u = request.user
    if not u.is_staff and not u.is_superuser:
        return HttpResponse('非管理员 无操作权限')

    try:
        book_id = request.GET['id']
    except KeyError:
        book_id = 1

    try:
        prefix = request.GET['prefix']
    except KeyError:
        prefix = 0

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
            name, author, digest = biqooge.get_a_chapter(book_id=book_id, prefix=prefix)
        except IndexError:
            return HttpResponse('该书不存在')
        new_book = Book.objects.create(
            book_id=book_id, book_name=name, author=author, digest=digest, current=current_chapter)
        new_book.save()

    return HttpResponse(f'{name, author, digest}')


def get_content(request):
    # 爬内容了 自用
    try:
        u = request.user
        if not u.is_staff and not u.is_superuser:
            return HttpResponse('非管理员 无操作权限')
        get_dict = request.GET

        if not get_dict:
            return HttpResponse('id(book_id), prefix(biqooge的url prefix_book_id), target(爬几章)')

        book_id = get_dict.get('id') or 1
        prefix = get_dict.get('prefix') or 0
        try:
            target = int(get_dict.get('target')) or 1
        except ValueError:
            return HttpResponse('target(爬取章节数)必须为整数')
        t1 = time.time()

        try:
            book1 = Book.objects.get(book_id=book_id)
        except ObjectDoesNotExist:
            return HttpResponse('还没这本书的简介 先去get_chapter')
        current_chapter = book1.current

        if book1.using:
            return HttpResponse('该书内容写入中 稍后再试')
        else:
            book1.using = True
            book1.save()

        #
        try:
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

            book1.using = False
            book1.save()
            r = f'已爬取 {count} 章,当前待爬取章节数为 {book1.current}, 用时{round(time.time() - t1, 2)}秒'
            return HttpResponse(r)

        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            book1.using = False
            book1.save()
            return HttpResponse(e)

    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        return HttpResponse(e)


def book(request):
    # 目录
    data = {'book_name': 0}
    u = request.user
    if u.is_authenticated:
        data.update({'username': u.username, 'user_img': u.img})
    url = request.path
    if not url.endswith(r'/'):
        url += '/'

    book_id = int(url.split('/')[-2])
    try:
        book1 = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return render(request, 'crawlers/book.html', data)
    # books = Book.objects.filter(book_id=book_id)
    # if len(books) == 0:
    #     return render(request, 'crawlers/book.html', data)
    else:
        # book1 = books[0]
        sets = BookContent.objects.filter(book_name_id=book_id)
        chapters = [x.chapter for x in sets]
        data.update({
            'book_id': book1.book_id,
            'book_name': book1.book_name,
            'author': book1.author,
            'digest': book1.digest,
            'read_count': book1.read_count,
            'collect_count': book1.collect_count,
            'current': book1.current,
            'chapters': chapters,
        })

        # print(data)

        return render(request, 'crawlers/book.html', data)


def books(request):
    data = {}
    # u = login_check(request)
    u = request.user
    if u.is_authenticated:
        data.update({'username': u.username, 'user_img': u.img})
        user_collections = json.loads(u.collections)
    else:
        user_collections = []

    all_books = Book.objects.all()
    all_books = [[x.book_name, x.book_id] for x in all_books]

    data.update({
        'all_books': all_books,
        'collections': user_collections,
    })

    # print(data, u)
    return render(request, 'crawlers/books.html', data)


def book_content(request):
    data = {'content': ''}
    u = request.user
    if u.is_authenticated:
        data.update({'username': u.username, 'user_img': u.img})

    url = request.path
    if not url.endswith(r'/'):
        url += '/'
    book_id = int(url.split('/')[-3])
    chapter = int(url.split('/')[-2])

    contents = BookContent.objects.filter(book_name_id=book_id, chapter_count=chapter)
    book1 = Book.objects.get(book_id=book_id)
    data.update({
        'book_id': book_id,
        'book_name': book1.book_name,
        'chapter_count': chapter,
    })
    if len(contents) == 0:
        return render(request, 'crawlers/content.html', data)
    else:
        content = contents[0]
        data.update({
            'chapter': content.chapter,
            'chapter_count': content.chapter_count,
            'content': content.content,
            'collect_count': content.collect_count,
            'read_count': content.read_count,
        })

        data['comments'] = []
        comments = Comment.objects.filter(book_id=book_id, chapter_count=chapter)
        for comment in comments:
            temp = {
                'id': comment.id,
                'book_id': comment.book_id,
                'chapter_count': comment.chapter_count,
                'user_name': comment.user_name,
                'comment': comment.comment,
                'ts': comment.ts,
                'agree': comment.agree,
            }
            data['comments'].append(temp)

        content.read_count += 1
        content.save()
        book1.read_count += 1
        book1.save()
        # print(data['comments'])

        return render(request, 'crawlers/content.html', data)
