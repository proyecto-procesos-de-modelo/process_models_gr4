
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout


from global_login_required import login_not_required

from storage_go_project.storage_go_app import forms as storage_forms


# Create your views here.
@login_not_required
def home(request):
    """
    """

    return render(request, 'home.html', {})


@login_not_required
def custom_login(request):
    """
    """

    title = 'Acceso'
    if request.method == 'POST':
        form = storage_forms.LoginForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect('panel:shipper_list')

    else:
        form = storage_forms.LoginForm()

    return render(request, 'login.html', {
        'title': title,
        'form': form,
    })


class CustomDetailView(View):
    """
    """

    element = None
    model = None
    urls = None

    def get(self, request, id=None, *args, **kwargs):
        """
        """

        title = "Ver "
        title += self.model._meta.verbose_name

        self.element = get_object_or_404(self.model, id=id)

        fields = []
        model_fields = self.model._meta.get_fields()
        exclude_fields = getExcludeFields(self.model._meta.verbose_name_plural, 'view')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]
        print(fields)

        list = {}
        for field in fields:
            if field.__class__.__name__ in shipping_config.related_fields:
                values = []
                for value in getattr(self.element, field.name).all():
                    values.append(str(value))
                list[field.verbose_name] = values
            else:
                list[field.verbose_name] = getattr(self.element, field.name)
        self.element.fields_values = list

        return render(request, 'view.html', {
        'title': title,
        'element': self.element,
    })


class CustomDeleteView(View):
    """
    """

    model = None
    urls = None
    element = None

    def post(self, request, id=None, *args, **kwargs):
        """
        """

        self.urls = getUrls(self.model._meta.verbose_name_plural)

        self.element = get_object_or_404(self.model, id=id)

        title = "Borrar "
        title += self.model._meta.verbose_name

        form = shipping_forms.ConfirmationForm(request.POST)

        if form.is_valid():
            self.element.delete()

            return redirect(getRedirectUrl(self.model._meta.verbose_name_plural))

        else:
            print("formulario invalido")

        return render(request, 'delete.html', {
            'title': title,
            'form': form,
            'urls': self.urls,
            'element': self.element
        })

    def get(self, request, id=None, *args, **kwargs):
        """
        """

        title = "Borrar "
        title += self.model._meta.verbose_name

        self.urls = getUrls(self.model._meta.verbose_name_plural)

        self.element = get_object_or_404(self.model, id=id)

        form = shipping_forms.ConfirmationForm()

        return render(request, 'delete.html', {
        'title': title,
        'element': self.element,
        'form': form,
        'urls': self.urls
    })

