import datetime
import time

# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.http import QueryDict
from django.utils import timezone

from account.models import User
from crawlers.models import Book, BookContent, Comment
import json
# Create your views here.


def user_collections(request):
    # 获取/添加收藏 获取需要u 添加需要u book_id chapter_count
    res = {
        'result': False,
        'data': [],
        'msg': '',
    }
    if request.method == "GET":
        # u
        get_dict = request.GET
        user_name = get_dict.get('u')
        if not user_name:
            # 未提供u(user_name)字段
            res['msg'] = '未提供u(user_name)字段'
            return JsonResponse(res)

        users = User.objects.filter(username=user_name)
        if len(users) == 0:
            # 没有该user_name
            res['msg'] = f'没有该user_name {user_name} '
            return JsonResponse(res)

        else:
            user1 = users[0]
            res['result'] = True
            res['data'] = json.loads(user1.collections)
            # print(res)
            return JsonResponse(res)

    elif request.method == "POST":
        # u book_id chapter_count
        post_dict = request.POST
        # print(post_dict)
        user_name = post_dict.get('u')
        if not user_name:
            # 未提供u(user_name)字段
            res['msg'] = '未提供u(user_name)字段'
            return JsonResponse(res)

        users = User.objects.filter(username=user_name)
        if len(users) == 0:
            # 没有该user_name
            res['msg'] = f'没有该user_name {user_name} '
            return JsonResponse(res)

        else:
            user1 = users[0]
            # [{'book_id': 0, 'book_name': '', 'chapter_count': '', 'ts': 0}]
            book_id = post_dict.get('book_id')
            chapter_count = post_dict.get('chapter_count')
            try:
                chapter_count = int(chapter_count)
                book_id = int(book_id)
            except TypeError:
                # 不是整数
                res['msg'] = f'book_id {book_id} 或 chapter_count {chapter_count} 不是整数'
                return JsonResponse(res)

            books = Book.objects.filter(book_id=book_id)
            if not books:
                # 没有对应书目
                res['msg'] = f'没有对应书目 {book_id}'
                return JsonResponse(res)

            book1 = books[0]
            chapters = BookContent.objects.filter(book_name_id=book_id, chapter_count=chapter_count)
            if not chapters:
                # 没有对应章节
                res['msg'] = f'没有该章节号 {chapter_count}'
                return JsonResponse(res)

            append = {
                'book_id': book_id,
                'book_name': book1.book_name,
                'chapter': chapters[0].chapter,
                'chapter_count': chapter_count,
                'ts': time.time()
            }

            temp_str = user1.collections
            temp_list = json.loads(temp_str)

            # 重复检测
            bid_ch = [(x['book_id'], x['chapter_count']) for x in temp_list]
            # print(bid_ch)
            if (book_id, chapter_count) in bid_ch:
                res['msg'] = f'该章节{book_id, chapter_count}已存在收藏夹 {bid_ch} 中'
                return JsonResponse(res)

            temp_list.append(append)
            user1.collections = json.dumps(temp_list)
            user1.save()
            res['result'] = True
            res['data'] = append
            res['msg'] = '成功加入收藏夹'

            return JsonResponse(res)

    # elif request.method == 'DELETE':
    #     delete_dict = request.DELETE
    #     print(delete_dict)
    #     return JsonResponse(res)
    else:
        res['msg'] = 'method "get" or "post" accepted'
        return JsonResponse(res)


class UserCollections(View):
    # 用户收藏

    def get(self, request, book_id, chapter_count):
        # 不太需要get...
        res = {
            'result': False,
            'data': [],
            'msg': '',
        }
        get_dict = request.GET
        user_name = get_dict.get('u')
        if not user_name:
            # 未提供u(user_name)字段
            res['msg'] = '未提供u(user_name)字段'
            return JsonResponse(res)

        users = User.objects.filter(username=user_name)
        if len(users) == 0:
            # 没有该user_name
            res['msg'] = f'没有该user_name {user_name} '
            return JsonResponse(res)

        else:
            user1 = users[0]
            res['result'] = True
            res['data'] = json.loads(user1.collections)
            # print(res)
            return JsonResponse(res)

    def post(self, request, book_id, chapter_count):
        res = {
            'result': False,
            'data': [],
            'msg': '',
        }

        post_dict = request.POST
        user_name = post_dict.get('u')
        if not user_name:
            # 未提供u(user_name)字段
            res['msg'] = '未提供u(user_name)字段'
            return JsonResponse(res)

        users = User.objects.filter(username=user_name)
        if len(users) == 0:
            # 没有该user_name
            res['msg'] = f'没有该user_name {user_name} '
            return JsonResponse(res)

        else:
            user1 = users[0]
            # [{'book_id': 0, 'book_name': '', 'chapter_count': '', 'chapter': '', 'ts': 0}]
            try:
                chapter_count = int(chapter_count)
                book_id = int(book_id)
            except TypeError:
                # 章节数chapter_count不是整数
                res['msg'] = f'章节数chapter_count不是整数'
                return JsonResponse(res)

            books = Book.objects.filter(book_id=book_id)
            if not books:
                # 没有对应书目
                res['msg'] = f'没有对应书目 {book_id}'
                return JsonResponse(res)

            book1 = books[0]
            chapters = BookContent.objects.filter(book_name_id=book_id, chapter_count=chapter_count)
            if not chapters:
                # 没有对应章节
                res['msg'] = f'没有该章节号 {chapter_count}'
                return JsonResponse(res)

            append = {
                'book_id': book_id,
                'book_name': book1.book_name,
                'chapter_count': chapter_count,
                'chapter': chapters[0].chapter,
                'ts': time.time()
            }

            temp_str = user1.collections
            temp_list = json.loads(temp_str)

            # 重复检测
            bid_ch = [(x['book_id'], x['chapter_count']) for x in temp_list]
            # print(bid_ch)
            if (book_id, chapter_count) in bid_ch:
                res['msg'] = f'该章节{book_id, chapter_count}已存在收藏夹 {bid_ch} 中'
                return JsonResponse(res)

            temp_list.append(append)
            user1.collections = json.dumps(temp_list)
            user1.save()
            res['result'] = True
            res['data'] = append
            res['msg'] = '成功加入收藏夹'

            return JsonResponse(res)

    def delete(self, request, book_id, chapter_count):
        res = {
            'result': False,
            'data': [],
            'msg': '',
        }

        # tricky 应该自己写个小轮子拆k, v
        dic = QueryDict(request.body.decode())
        # return JsonResponse(dic)
        user_name = dic.get('u')
        if not user_name:
            # 未提供u(user_name)字段
            res['msg'] = '未提供u(user_name)字段'
            return JsonResponse(res)

        users = User.objects.filter(username=user_name)
        if len(users) == 0:
            # 没有该user_name
            res['msg'] = f'没有该user_name {user_name} '
            return JsonResponse(res)

        else:
            user1 = users[0]
            # [{'book_id': 0, 'book_name': '', 'chapter_count': '', 'ts': 0}]
            try:
                chapter_count = int(chapter_count)
                book_id = int(book_id)
            except TypeError:
                # 章节数chapter_count不是整数
                res['msg'] = f'章节数chapter_count不是整数'
                return JsonResponse(res)

            books = Book.objects.filter(book_id=book_id)
            if not books:
                # 没有对应书目
                res['msg'] = f'没有对应书目 {book_id}'
                return JsonResponse(res)

            # book1 = books[0]
            chapters = BookContent.objects.filter(book_name_id=book_id, chapter_count=chapter_count)
            if not chapters:
                # 没有对应章节
                res['msg'] = f'没有该章节号 {chapter_count}'
                return JsonResponse(res)

            temp_str = user1.collections
            temp_list = json.loads(temp_str)

            # 看有没有对应的
            # print(bid_ch)
            # print(temp_list)
            # print(book_id, chapter_count)
            for record in temp_list:
                # print(record['book_id'], record['chapter_count'])
                if record['book_id'] == book_id and record['chapter_count'] == chapter_count:
                    temp_list.remove(record)
                    user1.collections = json.dumps(temp_list)
                    user1.save()
                    res['result'] = True
                    res['msg'] = '成功从收藏夹中移除'
                    return JsonResponse(res)
                else:
                    pass
            res['msg'] = '收藏夹里没有该内容'
            return JsonResponse(res)


class CommentApi(View):
    # 评论
    @staticmethod
    def blank_dict():
        return dict(result=False, data=list(), msg=str())

    def get(self, request, book_id, chapter_count):
        res = self.blank_dict()

        try:
            chapter_count = int(chapter_count)
            book_id = int(book_id)
        except TypeError:
            # 不是整数
            res['msg'] = f'book_id {book_id} 或 chapter_count {chapter_count} 不是整数'
            return JsonResponse(res)
        comments = Comment.objects.filter(book_id=book_id, chapter_count=chapter_count)
        for comment in comments:
            res['data'].append({
                'id': comment.id,
                'user_name': comment.user_name,
                'comment': comment.comment,
                'ts': comment.ts,
                'agree': comment.agree,
            })
        res['result'] = True
        return JsonResponse(res)

    def post(self, request, book_id, chapter_count):
        res = self.blank_dict()
        try:
            chapter_count = int(chapter_count)
            book_id = int(book_id)
        except TypeError:
            # 不是整数
            res['msg'] = f'book_id {book_id} 或 chapter_count {chapter_count} 不是整数'
            return JsonResponse(res)

        post_dict = request.POST
        user_name = post_dict.get('u')
        comment = post_dict.get('comment')
        if comment is None:
            comment = ''
        # if user_name is None:
        #     user_name = ''

        try:
            user1 = User.objects.get(username=user_name)
        except User.DoesNotExist:
            user1 = False

        new_comment = Comment.objects.create(
            book_id=book_id,
            chapter_count=chapter_count,
            comment=comment,
            # ts=datetime.datetime.now(),
            ts=timezone.now(),
        )
        if user_name:
            new_comment.user_name = user_name
        new_comment.save()

        res['result'] = True
        res['msg'] = 'add comment successfully'

        if user1:
            user1.comments += 1
            user1.save()
        return JsonResponse(res)

    def put(self, request, book_id, chapter_count):
        # 如果一定要修改评论
        res = self.blank_dict()
        try:
            chapter_count = int(chapter_count)
            book_id = int(book_id)
        except TypeError:
            # 不是整数
            res['msg'] = f'book_id {book_id} 或 chapter_count {chapter_count} 不是整数'
            return JsonResponse(res)

        dic = QueryDict(request.body.decode())
        user_name = dic.get('u')
        comment = dic.get('comment')
        comment_id = dic.get('id')
        try:
            comment_id = int(comment_id)
        except TypeError:
            res['msg'] = f'id(comment_id) should be an integer'
            return JsonResponse(res)

        if comment is None:
            comment = ''
        if not user_name:
            # 未提供u(user_name)字段
            res['msg'] = '未提供u(user_name)字段'
            return JsonResponse(res)

        users = User.objects.filter(username=user_name)
        if len(users) == 0:
            # 没有该user_name
            res['msg'] = f'没有该user_name {user_name} '
            return JsonResponse(res)
        else:
            try:
                comment1 = Comment.objects.get(id=comment_id)
            except Comment.DoesNotExist:
                res['msg'] = 'this id(comment_id) does not exists.'
                return JsonResponse(res)
            comment1.comment = comment
            comment1.ts = timezone.now()
            res['result'] = True
            res['msg'] = 'put comment successfully'
            comment1.save()
            return JsonResponse(res)

    def delete(self, request, book_id, chapter_count):
        # 如果一定要修改评论
        res = self.blank_dict()
        try:
            chapter_count = int(chapter_count)
            book_id = int(book_id)
        except TypeError:
            # 不是整数
            res['msg'] = f'book_id {book_id} 或 chapter_count {chapter_count} 不是整数'
            return JsonResponse(res)

        dic = QueryDict(request.body.decode())
        user_name = dic.get('u')
        comment = dic.get('comment')
        comment_id = dic.get('id')
        try:
            comment_id = int(comment_id)
        except TypeError:
            res['msg'] = f'id(comment_id) should be an integer'
            return JsonResponse(res)

        if comment is None:
            comment = ''
        if not user_name:
            # 未提供u(user_name)字段
            res['msg'] = '未提供u(user_name)字段'
            return JsonResponse(res)

        users = User.objects.filter(username=user_name)
        if len(users) == 0:
            # 没有该user_name
            res['msg'] = f'没有该user_name {user_name} '
            return JsonResponse(res)
        else:
            try:
                comment1 = Comment.objects.get(id=comment_id)
            except Comment.DoesNotExist:
                res['msg'] = 'this id(comment_id) does not exists.'
                return JsonResponse(res)
            comment1.delete()
            res['result'] = True
            res['msg'] = 'delete comment successfully'
            return JsonResponse(res)
