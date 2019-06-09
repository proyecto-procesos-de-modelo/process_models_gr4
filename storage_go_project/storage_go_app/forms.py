#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group

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


class CustomPermissionForm(forms.Form):
    """
    """

    group = forms.ChoiceField(label='Grupo', widget=forms.Select())
    TYPE = (('Modelo', 'Modelo'), ('Objeto', 'Objeto'), ('Atributo', 'Atributo'))
    type = forms.ChoiceField(label='Tipo', choices=TYPE, widget=forms.Select())
    ACTION = (('Ver', 'Ver'), ('Filtrar', 'Filtrar'), ('Crear', 'Crear'), ('Modificar', 'Modificar'), ('Borrar','Borrar'))
    action = forms.ChoiceField(label='Acción', choices=ACTION, widget=forms.Select())
    VOID = (('Todos', 'Todos'),)
    model = forms.ChoiceField(label='Modelo', choices=VOID, widget=forms.Select())
    object = forms.ChoiceField(label='Objeto', choices=VOID, required=False, widget=forms.Select())
    attribute = forms.ChoiceField(label='Atributo', choices=VOID, required=False, widget=forms.Select())

    def __init__(self, *args, **kwargs):
        """
        """

        from django.apps import apps
        from collections import OrderedDict

        super(CustomPermissionForm, self).__init__(*args, **kwargs)

        list = Group.objects.all()
        groups = []
        for model in list:
            aux_tuple = (model.name, model.name)
            groups.append(aux_tuple)

        self.fields['group'] = forms.ChoiceField(choices=groups)

        dict = apps.all_models['storage_go_app']
        models = []
        for model in dict.items():
            aux_tuple = (model[1]._meta.verbose_name, model[1]._meta.verbose_name)
            models.append(aux_tuple)

        self.fields['model'] = forms.ChoiceField(choices=models)


class ProductCustomCreateForm(forms.ModelForm):
    """
    """

    exit_date = forms.DateField(widget=forms.TextInput(attrs={'placeholder': '31/12/20019', 'class': 'datepicker'}))

    class Meta:
        model = storage_models.Product
        fields = '__all__'


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
