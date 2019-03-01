from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from .forms import CustomUserCreationForm, CustomUserChangeForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


class UpdateProfile(LoginRequiredMixin, generic.UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('profile')
    template_name = 'users/profileedit.html'

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def profile(request):
    return render(request, 'users/profile.html')
