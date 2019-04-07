
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.core.paginator import Paginator

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
