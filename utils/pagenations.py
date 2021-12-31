# -*- coding: utf-8 -*-
from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


class PageNum(LimitOffsetPagination):
    """limit offset"""
    default_limit = 5
    # limit_query_param = 'limit'
    # limit_query_description = _('Number of results to return per page.')
    # offset_query_param = 'offset'
    # offset_query_description = _('The initial index from which to return the results.')
    max_limit = 7


class PageNum1(PageNumberPagination):
    page_size_query_param = 'pagesize'
    max_page_size = 15

    def get_paginated_response(self, data):
        # return Response(OrderedDict([
        #     ('count', self.page.paginator.count),
        #     ('next', self.get_next_link()),
        #     ('previous', self.get_previous_link()),
        #     ('results', data)
        # ]))
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('lists', data),
            ('page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('pagesize', self.page.paginator.per_page),
        ]))
