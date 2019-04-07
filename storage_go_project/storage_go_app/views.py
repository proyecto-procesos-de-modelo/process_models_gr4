from django.shortcuts import render
from storage_go_app import forms as customforms

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

