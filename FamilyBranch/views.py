from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.shortcuts import render, redirect

from .forms import RegistrationForm
from .models import Person


class HomeView(LoginRequiredMixin, View):
    template_name = 'index.html'
    login_url = '/user/login/'

    def get(self, request):
        ancestor = Person.objects.get_root_ancestor(request.user.pk)
        return render(request, self.template_name, {'parent_id': ancestor.pk})


class RegistrationView(View):
    template_name = 'registration/registration.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name='User')
            user.groups.add(group)

            user.is_staff = True
            user.username = form.cleaned_data.get('email')
            user.save()

            return redirect('/user/login')
        return render(request, self.template_name, {'form': form})
