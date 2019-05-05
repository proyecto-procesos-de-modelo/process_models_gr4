#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from storage_go_app import models as storage_models


# General Forms
class LoginForm(AuthenticationForm):
    """
    """

    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': u'Nombre de Usuario'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': u'Contraseña'}))


class ResetForm(forms.Form):
    """
    """
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Nombre de usuario o correo electrónico'}))


class ResetPasswordForm(forms.Form):
    """
    """

    username = forms.CharField(label="", widget=forms.HiddenInput)
    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': u'Contraseña'}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': u'Confirmar contraseña'}))


class ConfirmationForm(forms.Form):
    """
    """

    ok = forms.IntegerField(widget=forms.HiddenInput(), initial=1, label='')


class CustomPermissionForm(forms.ModelForm):
    """
    """

    #type
    #action
    #model = forms.ChoiceField(label='Modelo', required=False, widget=forms.Select())
    object = forms.ChoiceField(label='Objeto', required=False, widget=forms.Select())
    attribute = forms.ChoiceField(label='Atributo', required=False, widget=forms.Select())

    class Meta:
        model = storage_models.CustomPermission
        fields = ('type', 'action', 'model')#, 'object', 'attribute')

    def __init__(self, *args, **kwargs):
        """
        """

        from django.apps import apps
        from collections import OrderedDict

        super().__init__(*args,**kwargs)

        dict = apps.all_models['storage_go_app']
        models = []
        for model in dict.items():
            aux_tuple = (model[1]._meta.verbose_name, model[1]._meta.verbose_name)
            models.append(aux_tuple)

        self.fields['model'] = forms.ChoiceField(
            choices=models,
            label='Modelo',
            widget=forms.Select()
        )

        #OBEJCTS = model.
        #object = forms.ChoiceField(choices=OBEJCTS, label='Módulo', widget=forms.Select())

        #ATTRIBUTES = object.get_fields
        #attribute = forms.ChoiceField(choices=ATTRIBUTES, label='Tipo', widget=forms.Select())



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
