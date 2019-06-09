
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import json

from storage_go_app import api
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.models import Group, User
from django.apps import apps
from django.contrib.contenttypes.models import ContentType

from global_login_required import login_not_required

from storage_go_app import forms as storage_forms
from storage_go_app import permissions as storage_permissions
from storage_go_app import utilities as storage_utilities
from storage_go_app import config as storage_config
from storage_go_app import models as storage_models
from storage_go_app import procedures as storage_procedures

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

                    user = get_object_or_404(User, id=request.user.id)
                    group = user.groups.all()
                    return redirect(str(storage_utilities.getProfileRedirectUrl(group[0])))

    else:
        form = storage_forms.LoginForm()

    return render(request, 'login.html', {
        'title': title,
        'form': form,
    })


# Map Views
def map(request):
    """
    """

    return render(request, 'map.html', {})


def fichar(request, id=None):
    """
    """

    print("fichar function")

    try:
        active_user = get_object_or_404(storage_models.ActiveUser, user_id=id)
        print(active_user)
        active_user.delete()
    except:
        storage_models.ActiveUser.objects.create(user_id=id)

    #return redirect(request, 'map.html', {})
    return redirect('panel:map')


# Statistics Views
def general_statistics(request):
    """
    """

    import json
    from django.db import connection
    from datetime import date, timedelta

    print("general statistics function")

    today = date.today()
    first_day = today - timedelta(days=today.weekday())
    last_day = first_day + timedelta(days=6)

    print(today)
    print(first_day)
    print(last_day)

    title = 'Estadísticas'
    statistics = {}

    ##### Active Users
    cursor = connection.cursor()
    response = cursor.execute(' \
        SELECT g.name, COUNT(ug.group_id) as num_active_user \
        FROM auth_group g, active_user au \
        LEFT JOIN auth_user_groups ug \
        ON g.id == ug.group_id \
        AND ug.user_id == au.user_id \
        GROUP BY g.name; \
    ')
    aux = response.fetchall()

    element = {}
    aux2 = []

    for item in aux:
        element['group'] = item[0]
        element['users'] = item[1]
        aux2.append(element)
        element = {}

    statistics['active_users'] = aux2

    ##### Move Tasks
    statistics['move_tasks'] = 0

    ##### Entry Products
    response = cursor.execute(' \
        WITH RECURSIVE dates(date) AS ( \
        VALUES(date("now", "weekday 1", "-7 days")) \
        UNION ALL \
        SELECT date(date, "+1 day") \
        FROM dates \
        WHERE date < date("now", "weekday 0")) \
        SELECT d.date, COUNT(p.entry_date) as num_products \
        FROM dates d \
        LEFT JOIN product p \
        ON d.date == p.entry_date \
        GROUP BY d.date \
        ORDER BY d.date ASC; \
    ')
    aux = response.fetchall()

    element = {}
    aux2 = []

    for item in aux:
        element['date'] = item[0]
        element['num_products'] = item[1]
        aux2.append(element)
        element = {}

    statistics['entry_products'] = aux2

    # exit products

    # SLA

    ##### % rooms ocupation
    response = cursor.execute('')
    aux = response.fetchall()

    element = {}
    aux2 = []

    for item in aux:
        element['name'] = item[0]
        element['percent'] = item[1]
        aux2.append(element)
        element = {}

    statistics['rooms_ocupation'] = aux2

    print(statistics)

    return render(request, 'statistics.html', {
        'title': title,
        'statistics': statistics,
    })


def map_statistics(request):
    """
    """

    print("general statistics function")

    title = 'Estadísticas'

    return render(request, 'statistics.html', {
        'title': title
    })


# Customized Views
def download_data(request, id=None):
    """
    https://realpython.com/python-requests/
    https://realpython.com/python-json/
    """

    print("api function")

    title = 'Información de la API'
    data = api.query()

    for ref in data:
        if ref['withdrawal'] == True:
            print("salida")
            # obtenemos los contenedores
            for product in ref['Products']:
                print(product)
                product = get_object_or_404(storage_models.Product, name=product['name'])
                print(product)
                containers = storage_models.Container.objects.filter(product_id=product.id)
                print(containers)

                for container in containers:
                    destination = storage_models.RoomMap.objects.filter(room_id=34, status='Disponible').order_by('id').first()
                    print(destination)

                    move_task = storage_models.MoveTask.objects.create(
                        container = container,
                        destination = destination
                    )

        else:
            print("entrada")
            # Creamos los productos
            for product in ref['Products']:
                num_containers = int(product['qty'])

                print(product['sla'])
                print(product['sla'].split('T')[0])

                product, created = storage_models.Product.objects.get_or_create(
                    name = product['name'],
                    exit_date = product['sla'].split('T')[0],
                    min_humidity = product['humidMin'],
                    max_humidity = product['humidMax'],
                    min_temperature = product['tempMinDegree'],
                    max_temperature = product['tempMaxDegree'],
                    num_containers = num_containers
            )

    return render(request, 'api_info.html', {
        'title': title,
        'data': data,
    })


def permission_create(request):
    """
    """

    print("custom create permissions view")

    urls = storage_utilities.getUrls('Permisos Personalizados')

    title = "Crear Permiso"

    if request.method == 'POST':
        print("POST")

        form = storage_forms.CustomPermissionForm(request.POST)
        print(form)
        if form.is_valid():
            print("form valid")
            data = form.cleaned_data
            print(data)
            #form.save()

            group = get_object_or_404(Group, name=data['group'])

            custom_permission = storage_models.CustomPermission.objects.create(
                group = group,
                type = data['type'],
                action = data['action'],
                model = data['model'],
                object = data['object'],
                attribute = data['attribute'],
            )

            return redirect('panel:permission_list')

        else:
            print("form invalid")
            print(form.errors)

    else:
        print("GET")
        form = storage_forms.CustomPermissionForm()

    return render(request, 'create_permissions.html', {
        'title': title,
        'form': form,
        'urls': urls,
    })


def permission_load(request):
    """
    """

    print("custom load permissions view")

    from django.apps import apps
    from django.http import HttpResponse
    #from django.core import serializers
    from django.contrib.contenttypes.models import ContentType
    import json


    type = request.GET.get('type', None)
    print(type)
    model = request.GET.get('model', None)
    print(model)
    object = request.GET.get('object', None)
    print(object)

    data = None

    if type == 'Modelo': # si el tipo es de modelo
        print("type model")
        content_types = ContentType.objects.filter(app_label='storage_go_app')
        list = []
        for model in content_types:
            aux_tuple = (model.id, str(model))
            list.append(aux_tuple)
        data = json.dumps(list)
        print("return models")
        print(data)

        return HttpResponse(data, content_type='application/json')

    elif type == 'Objeto':
        print("type object")
        if model == '':
            print("model is none")
            content_types = ContentType.objects.filter(app_label='storage_go_app')
            print(content_types)
            list = []
            for model in content_types:
                aux_tuple = (str(model.model), str(model))
                list.append(aux_tuple)
            data = json.dumps(list)
            print("return models")
            print(data)

            return HttpResponse(data, content_type='application/json')

        else:
            print("model is not none")
            objects = None
            content_type = get_object_or_404(ContentType, model=model)
            print(content_type)
            model = apps.get_model('storage_go_app', content_type.model)
            objects = model.objects.all()

            list = []
            for object in objects:
                aux_tuple = (str(object.__str__()), str(object.__str__()))
                list.append(aux_tuple)
            data = json.dumps(list)
            print("return objects")
            print(data)

            return HttpResponse(data, content_type='application/json')

    elif type == 'Atributo':
        print("type attribute")

        if model == '':
            print("model is none")
            content_types = ContentType.objects.filter(app_label='storage_go_app')
            list = []
            for model in content_types:
                aux_tuple = (model.id, str(model))
                list.append(aux_tuple)
            data = json.dumps(list)
            print("return models")
            print(data)

            return HttpResponse(data, content_type='application/json')

        else:
            print("models is not none")
            content_type = get_object_or_404(ContentType, id=model)
            model = apps.get_model('storage_go_app', content_type.model)

            if object == '':
                print("object is none")
                objects = model.objects.all()
                list = []
                for object in objects:
                    aux_tuple = (object.id, str(object))
                    list.append(aux_tuple)
                data = json.dumps(list)
                print("return objects")
                print(data)

                return HttpResponse(data, content_type='application/json')

            else:
                print("object is not none")
                content_types = ContentType.objects.filter(app_label='storage_go_app')
                model = apps.get_model('storage_go_app', content_type.model)
                object = get_object_or_404(model, id=object)
                attributes = object._meta.fields #_meta.get_fields(include_parents=False)
                list = []
                for attribute in attributes:
                    aux_tuple = (str(attribute.verbose_name), str(attribute.verbose_name))
                    list.append(aux_tuple)
                data = json.dumps(list)
                print("return attributes")
                print(data)

                return HttpResponse(data, content_type='application/json')

    else:
        print("ninguno de lo anterior")
        return HttpResponse(data, content_type='application/json')

# Classes
class CustomDetailView(View):
    """
    """

    # Variables de la clase
    element = None
    model = None
    urls = None

    def get(self, request, id=None, *args, **kwargs):
        """
        Metodo get
        """

        print("custom detail view")

        room_map_elements = {}

        # Creamos el título
        title = "Ver "
        title += str(self.model._meta.verbose_name)

        # Obtenemos las Urls
        self.urls = storage_utilities.getUrls(self.model._meta.verbose_name_plural)

        # Obtenemos el elemento del que mostrar los detalles
        self.element = get_object_or_404(self.model, id=id)

        # Creamos una lista vacia para los atributos finales
        fields = []
        # Obtenemos los atributos del modelo
        model_fields = self.model._meta.get_fields()
        # Obtenemos los atributos que no queremos mostrar
        exclude_fields = storage_utilities.getExcludeFields(self.model._meta.verbose_name_plural, 'view')

        list = {}

        # Recorremos todos los attributos
        for field in model_fields:
            # Si se pueden mostrar
            if field.name not in exclude_fields:

                # Obtenemos el valor de los atributos dependiendo del tipo de atributo
                attribute_class_name = field.__class__.__name__

                if attribute_class_name == 'ManyToOneRel':

                    field_verbose_name = field.name.split('_')[0]
                    attribute_name = field_verbose_name+'_id'
                    content_type = get_object_or_404(ContentType, model=field.name.replace('_', ''))
                    object_model = apps.get_model('storage_go_app', content_type.model)
                    data = {
                        '{0}'.format(attribute_name): self.element.id,
                    }
                    room_map_elements = object_model.objects.filter(**data).order_by('x', 'y')

                else:
                    field_verbose_name = field.name
                    list[field.verbose_name] = getattr(self.element, field.name)

                # Comprobamos los permisos
                if storage_permissions.check_permissions(request.user.username, 'Atributo', 'Ver', self.model._meta.verbose_name, self.element.id, field_verbose_name):
                    fields.append(field)

        self.element.fields_values = list

        return render(request, 'view.html', {
        'title': title,
        'element': self.element,
        'model': self.model,
        'room_map': room_map_elements,
        'urls': self.urls
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

        print("custom list view function")

        #aux = storage_permissions.check_permissions(request)
        #print(aux)

        django_model = self.model

        title = self.model._meta.verbose_name_plural

        self.urls = storage_utilities.getUrls(self.model._meta.verbose_name_plural)

        if self.elements is None:
            elements = self.model.objects.all().order_by('-id')
        else:
            elements = self.elements

        order = request.GET.get('order')
        if order is not None:
            elements = elements.order_by(order)
        else:
            order = '-id'

        fields = []
        model_fields = self.model._meta.get_fields()
        exclude_fields = storage_utilities.getExcludeFields(self.model._meta.verbose_name_plural, 'list')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        for element in elements:
            list = []
            for field in fields:
                list.append(getattr(element, field.name))
            element.fields_values = list

        paginator = Paginator(elements, 50)
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
            'model': self.model._meta.verbose_name
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

        self.urls = storage_utilities.getUrls(self.model._meta.verbose_name_plural)

        self.element = get_object_or_404(self.model, id=id)

        title = "Borrar "
        title += str(self.model._meta.verbose_name)

        form = storage_forms.ConfirmationForm(request.POST)

        if form.is_valid():
            self.element.delete()

            return redirect(storage_utilities.getRedirectUrl(self.model._meta.verbose_name_plural))

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
        title += str(self.model._meta.verbose_name)

        self.urls = storage_utilities.getUrls(self.model._meta.verbose_name_plural)

        self.element = get_object_or_404(self.model, id=id)

        form = storage_forms.ConfirmationForm()

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
    check permissions to edit only permmited attributes
    """

    model = None
    urls = None

    def post(self, request, *args, **kwargs):
        """
        POST method
        """

        print("custom create function post")

        # Obtenemos las Urls
        #self.urls = storage_utilities.getUrls(self.model._meta.verbose_name_plural)

        # Obtenemos los attributos del elemento
        fields = []
        model_fields = self.model._meta.get_fields()
        # Obtenemos los atributos que no queremos mostrar
        exclude_fields = storage_utilities.getExcludeFields(self.model._meta.verbose_name_plural, 'create')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        form = storage_forms.get_custom_form(self.model, fields)
        form = form(request.POST)

        if form.is_valid():
            #data = form.cleaned_data
            form.save()

            return redirect(storage_utilities.getRedirectUrl(self.model._meta.verbose_name_plural))

        else:
            print("formulario invalido")
            print(form.errors)

        return render(request, 'create.html', {
            'form': form,
            #'urls': self.urls,
        })

    def get(self, request, *args, **kwargs):
        """
        GET method
        """

        print("custom create function")

        # Obtenemos los attributos del elemento
        fields = []
        model_fields = self.model._meta.get_fields()
        # Obtenemos los atributos que no queremos mostrar
        exclude_fields = storage_utilities.getExcludeFields(self.model._meta.verbose_name_plural, 'create')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        form = storage_forms.get_custom_form(self.model, fields)

        title = "Crear "
        title += self.model._meta.verbose_name

        self.urls = storage_utilities.getUrls(self.model._meta.verbose_name_plural)

        return render(request, 'create.html', {
            'title': title,
            'form': form,
            'urls': self.urls,
        })


class CustomFilterView(View):
    """
    """

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
                Q(id__gte=data['start_date']))

            if data['end_date'] is not None:
                elements = elements.filter(
                Q(id__lte=data['end_date']))

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

        return render(request, 'filter.html', {
            'title': title,
            'urls': urls,
            'form': form,
        })


class CustomUpdateView(View):
    """
    """

    model = None
    urls = None
    element = None

    def post(self, request, id=None, *args, **kwargs):
        """
        post method
        """

        print("custom update function")

        # Obtenemos las urls

        self.urls = storage_utilities.getUrls(self.model._meta.verbose_name_plural)

        # Obtenemos el elemento
        self.element = get_object_or_404(self.model, id=id)
        object = get_object_or_404(self.model, id=id)

        # Obtenemos los atributos
        fields = []
        model_fields = self.model._meta.get_fields()
        exclude_fields = storage_utilities.getExcludeFields(self.model._meta.verbose_name_plural, 'update')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        form = storage_forms.get_custom_form(self.model, fields)
        form = form(request.POST, instance=self.element)

        args = {}

        if form.is_valid():
            data = form.cleaned_data
            #print(data)

            for field in fields:
                #print(field)
                if field.name in data:
                    attribute_class_name = field.__class__.__name__
                    #print(attribute_class_name)
                    if attribute_class_name == 'ForeignKey':
                        attribute_name = field.name+'_id'
                        #attribute_name = str(self.model._meta.db_table) + '_' + str(field.name)
                    else:
                        attribute_name = field.name

                    #print(attribute_name)

                    data[field.name]
                    if data[field.name] is not None and data[field.name] != getattr(object, attribute_name) and data[field.name] != '':
                    #if data[field.name] != getattr(object, attribute_name):
                        #print("new value")
                        value = data[field.name]
                    else:
                        value = getattr(object, attribute_name)

                    args[attribute_name] = value

            object.custom_save(args)

            return redirect(storage_utilities.getRedirectUrl(self.model._meta.verbose_name_plural))

        else:
            print("formulario invalido")
            print(form.errors)

        return render(request, 'update.html', {
            'form': form,
            'urls': self.urls,
            'element': self.element
        })

    def get(self, request, id=None, *args, **kwargs):
        """
        get method
        generamos el formulario en funcion de los permisos que tiene cada usuario para modificar
        """

        print("custom update function")

        # Obtenemos las urls
        self.urls = storage_utilities.getUrls(self.model._meta.verbose_name_plural)

        # creamos el titulo
        title = "Editar "
        title += self.model._meta.verbose_name

        # Obtenemos el elemento
        self.element = get_object_or_404(self.model, id=id)

        # Obtenemos los atributos
        fields = []
        model_fields = self.model._meta.get_fields()
        #print(model_fields)
        exclude_fields = storage_utilities.getExcludeFields(self.model._meta.verbose_name_plural, 'update')

        # Comprobamos los permisos
        for field in model_fields:
            if field.name not in exclude_fields:
                field_verbose_name = self.model._meta.get_field(field.name).verbose_name
                if storage_permissions.check_permissions(request.user.username, 'Atributo', 'Modificar', self.model._meta.verbose_name, self.element.id, field_verbose_name):
                    fields.append(field)

        # creamos el formulario
        form = storage_forms.get_custom_form(self.model, fields)
        form = form(instance=self.element)

        return render(request, 'update.html', {
            'title': title,
            'form': form,
            'urls': self.urls,
            'element': self.element
        })


class ProductCustomCreateView(CustomCreateView):
    """
    """

    model = None
    urls = None

    def post(self, request, *args, **kwargs):
        """
        POST method
        """

        print("custom create function post")

        # Obtenemos las Urls
        #self.urls = storage_utilities.getUrls(self.model._meta.verbose_name_plural)

        # Obtenemos los attributos del elemento
        fields = []
        model_fields = self.model._meta.get_fields()
        # Obtenemos los atributos que no queremos mostrar
        exclude_fields = storage_utilities.getExcludeFields(self.model._meta.verbose_name_plural, 'create')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        #form = storage_forms.get_custom_form(self.model, fields)
        form = storage_forms.ProductCustomCreateForm(request.POST)
        #form = form(request.POST)

        if form.is_valid():
            #data = form.cleaned_data
            form.save()

            return redirect(storage_utilities.getRedirectUrl(self.model._meta.verbose_name_plural))

        else:
            print("formulario invalido")
            print(form.errors)

        return render(request, 'create.html', {
            'form': form,
            #'urls': self.urls,
        })

    def get(self, request, *args, **kwargs):
        """
        GET method
        """

        print("custom create function")

        # Obtenemos los attributos del elemento
        fields = []
        model_fields = self.model._meta.get_fields()
        # Obtenemos los atributos que no queremos mostrar
        exclude_fields = storage_utilities.getExcludeFields(self.model._meta.verbose_name_plural, 'create')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        #form = storage_forms.get_custom_form(self.model, fields)
        form = storage_forms.ProductCustomCreateForm()

        title = "Crear "
        title += self.model._meta.verbose_name

        self.urls = storage_utilities.getUrls(self.model._meta.verbose_name_plural)

        return render(request, 'create.html', {
            'title': title,
            'form': form,
            'urls': self.urls,
        })

def getValue(param):
    return str(param)




#
