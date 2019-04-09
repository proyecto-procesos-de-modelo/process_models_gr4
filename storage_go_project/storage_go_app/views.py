
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
