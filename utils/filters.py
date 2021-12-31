# -*- coding: utf-8 -*-
from django_filters import FilterSet

from users.models import User as User_model


class UserFilter(FilterSet):
    class Meta:
        model = User_model
        fields = {
            'username': ['exact', 'icontains'],
            'id': ['exact', 'lt', 'gt']
        }