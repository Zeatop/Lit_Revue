from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import ListView, View
from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from website.models import Ticket, Review
from itertools import chain
from operator import attrgetter

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('website:home')
   
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super().form_valid(form)

class MyLoginView(LoginView):
    redirect_authenticated_user = True
   
    def get_success_url(self):
        return reverse_lazy('website:home')
   
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

# class UserProfileView(LoginRequiredMixin, ListView):
#     template_name = 'users/user_profile.html'
#     context_object_name = 'contributions'

#     def get_queryset(self):
#         user = get_object_or_404(CustomUser, username=self.kwargs['username'])
#         tickets = Ticket.objects.filter(user=user)
#         reviews = Review.objects.filter(user=user)
#         contributions = sorted(
#             chain(tickets, reviews),
#             key=attrgetter('time_created'),
#             reverse=True
#         )
#         return contributions

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         profile_user = get_object_or_404(CustomUser, username=self.kwargs['username'])
#         context['profile_user'] = profile_user
#         context['is_following'] = self.request.user.is_following(profile_user)
#         return context


