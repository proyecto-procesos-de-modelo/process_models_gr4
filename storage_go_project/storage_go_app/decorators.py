#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import wraps
from django.db.models.signals import pre_save
from django.db.models.signals import post_save

def autoconnect(cls):
    """metodo que conecta automaticamen las señales con el modelo"""
    def connect(signal, func):
        cls.func = staticmethod(func)
        @wraps(func)
        def wrapper(sender, **kwargs):
            return func(kwargs.get('instance'))
        signal.connect(wrapper, sender=cls)
        return wrapper

    if hasattr(cls, 'pre_save'):
        cls.pre_save = connect(pre_save, cls.pre_save)

    if hasattr(cls, 'post_save'):
        cls.post_save = connect(post_save, cls.post_save)

    return cls
