#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# General Forms
class LoginForm(AuthenticationForm):
    """
    """

    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': u'Nombre de Usuario'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': u'Contraseña'}))


def get_custom_form(entry_model, entry_fields):
    """
    """

    fields_list = []
    [fields_list.append(field.name) for field in entry_fields]

    class _CustomForm(forms.ModelForm):

        class Meta:
            model = entry_model
            fields = fields_list

    return _CustomForm
