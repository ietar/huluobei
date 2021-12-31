# -*- coding: utf-8 -*-
from django.db.models import IntegerField


class UnsignedIntegerField(IntegerField):
    def db_type(self, connection):
        return 'integer UNSIGNED'
