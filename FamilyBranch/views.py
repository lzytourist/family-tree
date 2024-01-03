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
        if request.GET.get('person_id') is not None:
            parent_id = request.GET.get('person_id')
        else:
            try:
                person = Person.objects.filter(user_id=request.user.pk).first()
                ancestor = Person.objects.get_root_ancestor(person.pk)
                parent_id = ancestor.pk
            except Person.DoesNotExist:
                parent_id = None
        return render(request, self.template_name, {'parent_id': parent_id})


class RegistrationView(View):
    template_name = 'registration/registration.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            user.is_staff = True
            user.username = form.cleaned_data.get('email')
            user.save()

            group = Group.objects.get(name='User')
            user.groups.add(group)

            return redirect('/user/login')
        return render(request, self.template_name, {'form': form})
