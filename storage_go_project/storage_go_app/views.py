
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.core.paginator import Paginator

from global_login_required import login_not_required

from storage_go_app import forms as storage_forms

# Create your views here.
@login_not_required
def home(request):
    """
    """

    return render(request, 'home.html', {})


def activation(request, uidb64, token):
    """
    """

    print("activation function")

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        print("exception")
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        print("user is not None")
        user.is_active = True
        user.save()

        return redirect('cms:custom_login')

    else:
        print("user is None")
        print('Activation link is invalid!')
        return redirect('cms:home')


def password_reset(request):
    """
    """

    print("password reset function")

    if request.method == 'POST':
        print("post")

        form = cms_forms.ResetForm(request.POST)
        if form.is_valid():
            print("valid form")
            data = form.cleaned_data
            print(data['username'])

            user = User.objects.get(
                Q(username=data['username']) |
                Q(email=data['username']))

            if user is not None:
                print("user exist")
                if user.is_active:
                    print("user active")

                    current_site = get_current_site(request)
                    subject = 'Restablecer contraseña - Salamanca CMS'
                    from_email = settings.EMAIL_HOST_USER
                    to_email = [user.email,]
                    message = render_to_string('email_password_reset.txt', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                        'token': account_activation_token.make_token(user),
                    })
                    send_mail(subject, message, from_email, to_email, fail_silently=False,)

                else:
                    print("user not active")
            else:
                print("user not exist")
        else:
            print(form.errors)

        return redirect('cms:home')

    else:
        print("get")
        form = cms_forms.ResetForm()

    return render(request, 'password_reset.html', {
        'form': form,
    })


def password_reset_form(request, uidb64=None, token=None):
    """
    """

    print("passwrod reset form function")

    user = None

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        print("user not existe")
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'GET':
            print("get")
            form = cms_forms.ResetPasswordForm(initial={'username': user.username})

    else:
        if request.method == 'POST':
            print("post")

            form = cms_forms.ResetPasswordForm(request.POST)
            if form.is_valid():
                print("valid form")
                data = form.cleaned_data
                user = User.objects.get(username=data['username'])

                if data['password1'] == data['password2']:
                    print(data['password1'])
                    user.set_password(data['password1'])
                    user.save()

                current_site = get_current_site(request)
                subject = 'Confirmación - Salamanca CMS'
                from_email = settings.EMAIL_HOST_USER
                to_email = [user.email,]
                message = render_to_string('email_activation.txt', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                send_mail(subject, message, from_email, to_email, fail_silently=False,)

                return redirect('cms:home')

            else:
                print(form.errors)

    print(user)

    return render(request, 'password_reset_form.html', {
        'form': form,
    })


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

                    return redirect('panel:map')

    else:
        form = storage_forms.LoginForm()

    return render(request, 'login.html', {
        'title': title,
        'form': form,
    })


def map(request):
    """
    """

    return render(request, 'map.html', {})


def map_statistics(request):
    """
    """

    return render(request, 'map.html', {})


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

class CustomListView(View):
    """
    custom generic list view for all models
    order by attributes
    paginate the content
    show concrete attributes by model
    """

    elements = None
    model = None
    urls = None

    def get(self, request, *args, **kwargs):
        """
        """

        title = self.model._meta.verbose_name_plural

        self.urls = getUrls(self.model._meta.verbose_name_plural)

        if self.elements is None:
            elements = self.model.objects.all().order_by('-created_date')
        else:
            elements = self.elements

        order = request.GET.get('order')
        if order is not None:
            elements = elements.order_by(order)
        else:
            order = '-created_date'

        fields = []
        model_fields = self.model._meta.get_fields()
        exclude_fields = getExcludeFields(self.model._meta.verbose_name_plural, 'list')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]
        print(fields)

        for element in elements:
            list = []
            for field in fields:
                list.append(getattr(element, field.name))
            element.fields_values = list

        paginator = Paginator(elements, 10)
        page = request.GET.get('page')

        if page is None:
            page = 1

        try:
            elements = paginator.page(page)
        except PageNotAnInteger:
            elements = paginator.page(1)
        except EmptyPage:
            elements = paginator.page(paginator.num_pages)

        return render(request, 'list.html', {
            'elements': elements,
            'fields': fields,
            'urls': self.urls,
            'title': title,
            'order': order,
            'page': page,
	})

        model_fields = self.model._meta.get_fields()
        exclude_fields = getExcludeFields(self.model._meta.verbose_name_plural, 'update')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        form = shipping_forms.get_custom_form(self.model, fields)
        form = form(instance=self.element)

        title = "Editar "
        title += self.model._meta.verbose_name

        self.urls = getUrls(self.model._meta.verbose_name_plural)

        return render(request, 'update.html', {
            'title': title,
            'form': form,
            'urls': self.urls,
            'element': self.element
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


class CustomCreateView(View):
    """
    custom generic create view for all models
    generic crete form depends the model
    """

    model = None
    urls = None

    def post(self, request, *args, **kwargs):
        """
        """

        fields = []
        model_fields = self.model._meta.get_fields()
        exclude_fields = getExcludeFields(self.model._meta.verbose_name_plural, 'create')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        form = customforms.get_custom_form(self.model, fields)
        form = form(request.POST)

        if form.is_valid():
            form.save()

            return redirect(getRedirectUrl(self.model._meta.verbose_name_plural))

        else:
            print("formulario invalido")

        return render(request, 'create.html', {
            'form': form,
            'urls': self.urls,
        })

    def get(self, request, *args, **kwargs):
        """
        """

        fields = []
        model_fields = self.model._meta.get_fields()
        exclude_fields = getExcludeFields(self.model._meta.verbose_name_plural, 'create')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        form = customforms.get_custom_form(self.model, fields)

        title = "Crear "
        title += self.model._meta.verbose_name

        self.urls = getUrls(self.model._meta.verbose_name_plural)

        return render(request, 'create.html', {
            'title': title,
            'form': form,
            'urls': self.urls,
        })


class CustomFilterView(View):

    #title = 'Filtrar Categorías'
    #elements = cms_models.Categoria.objects.all()
    #urls = getCategoryUrls()

    model = None
    urls = None

    def post(self, request, *args, **kwargs):
        form = cms_forms.CategoryFilterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            if data['status'] is not None:
                elements = elements.filter(
                Q(estado=data['status']))

            if data['text'] is not None:
                elements = elements.filter(
                Q(titulo__icontains=data["text"]) |
                Q(en_titulo__icontains=data["text"]) |
                Q(subtitulo__icontains=data["text"]) |
                Q(en_subtitulo__icontains=data["text"]) |
                Q(informacion__icontains=data["text"]) |
                Q(en_informacion__icontains=data["text"]))

            if data['start_date'] is not None:
                elements = elements.filter(
                Q(created_date__gte=data['start_date']))

            if data['end_date'] is not None:
                elements = elements.filter(
                Q(created_date__lte=data['end_date']))

            if data['start_priority'] is not None:
                elements = elements.filter(
                Q(prioridad__gte=data['start_priority']))

            if data['end_priority'] is not None:
                elements = elements.filter(
                Q(prioridad__lte=data['end_priority']))

            if data['categoria_padre'] is not None:
                print(data['categoria_padre'])
                categoria_padre = get_object_or_404(cms_models.Categoria, titulo=data['categoria_padre'])
                print(categoria_padre.id)
                elements = elements.filter(categoria_padre_id=categoria_padre.id)
                #elements = elements.filter(categoria_padre=data['categoria_padre'])

            return None

    def get(self, request, *args, **kwargs):
        """
        """


        form = cms_forms.CategoryFilterForm()
    """
    return render(request, 'filter.html', {
        'title': title,
        'urls': urls,
        'form': form,
    })
    """


class CustomUpdateView(View):
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

        fields = []
        model_fields = self.model._meta.get_fields()
        exclude_fields = getExcludeFields(self.model._meta.verbose_name_plural, 'update')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        form = shipping_forms.get_custom_form(self.model, fields)
        form = form(request.POST, instance=self.element)

        if form.is_valid():
            form.save()

            return redirect(getRedirectUrl(self.model._meta.verbose_name_plural))

        else:
            print("formulario invalido")

        return render(request, 'update.html', {
            'form': form,
            'urls': self.urls,
            'element': self.element
        })

    def get(self, request, id=None, *args, **kwargs):
        """
        """

        self.urls = getUrls(self.model._meta.verbose_name_plural)

        self.element = get_object_or_404(self.model, id=id)

        fields = []
        model_fields = self.model._meta.get_fields()
        exclude_fields = getExcludeFields(self.model._meta.verbose_name_plural, 'update')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        form = shipping_forms.get_custom_form(self.model, fields)
        form = form(instance=self.element)

        title = "Editar "
        title += self.model._meta.verbose_name

        self.urls = getUrls(self.model._meta.verbose_name_plural)

        return render(request, 'update.html', {
            'title': title,
            'form': form,
            'urls': self.urls,
            'element': self.element
})
