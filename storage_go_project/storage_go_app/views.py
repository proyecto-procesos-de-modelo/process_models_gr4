
class CustomFilterView(View):
	
    title = 'Filtrar Categorías'
    elements = cms_models.Categoria.objects.all()
    urls = getCategoryUrls()

    if request.method == 'POST':
        print("POST")
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

            return category_list(request, elements)

        else:
            print("form invalid")

    else:
        print("GET")
        form = cms_forms.CategoryFilterForm()

    return render(request, 'filter.html', {
        'title': title,
        'urls': urls,
        'form': form,
    })    
