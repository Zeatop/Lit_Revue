from django.shortcuts import  redirect, get_object_or_404
from django.views.generic import (TemplateView, CreateView, UpdateView, DeleteView,
                                   DetailView, ListView, View)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from users.forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Review, Ticket
from .forms import NewTicketForm, ReviewForm, CombinedTicketReviewForm
from django.contrib.auth import get_user_model
from itertools import chain
from operator import attrgetter
from django import forms
from django.contrib import messages
from django.db.models import Q



User = get_user_model()

class UserProfileView(ListView):
    template_name = 'website/user_profile.html'
    context_object_name = 'contributions'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        tickets = Ticket.objects.filter(user=user)
        reviews = Review.objects.filter(user=user)
        contributions = sorted(
            chain(tickets, reviews),
            key=attrgetter('time_created'),
            reverse=True
        )
        return contributions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, username=self.kwargs['username'])
        return context

class SubscribeView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_to_follow = get_object_or_404(User, username=username)
        request.user.subscribe(user_to_follow)
        messages.success(request, f'Vous suivez maintenant {username}.')
        return redirect('website:user_profile', username=username)

class UnsubscribeView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_to_unfollow = get_object_or_404(User, username=username)
        request.user.unsubscribe(user_to_unfollow)
        messages.success(request, f'Vous ne suivez plus {username}.')
        return redirect('website:user_profile', username=username)

class FollowedUsersView(LoginRequiredMixin, ListView):
    template_name = 'website/followed_users.html'
    context_object_name = 'followed_users'

    def get_queryset(self):
        return self.request.user.followed_users.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')
        context['search_query'] = search_query
        
        if search_query:
            context['search_results'] = User.objects.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query)
            ).exclude(pk=self.request.user.pk)  # Exclure l'utilisateur actuel des résultats
        
        return context
    
class HomeView(TemplateView):
    """
    Vue pour la page d'accueil.
    Hérite de TemplateView pour une simple affichage de template.
    """
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        """
        Ajoute des formulaires d'inscription et de connexion au contexte.
        Cette méthode est appelée automatiquement lors du rendu de la vue.
        """
        context = super().get_context_data(**kwargs)
        context['register_form'] = RegisterForm()
        context['login_form'] = AuthenticationForm()

        tickets = Ticket.objects.all()
        reviews = Review.objects.all()
        combined_list = sorted(
            chain(tickets, reviews),
            key=attrgetter('time_created'),
            reverse=True
        )
        
        context['combined_feed'] = combined_list[:10]
        return context

class ActionContextMixin:
    """
    Mixin pour récupérer l'action en cours d'execution par l'utilisateur 
    """

    action = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = {'action': self.action}
        return context

class TicketCreateView(LoginRequiredMixin, ActionContextMixin, CreateView):
    model = Ticket
    form_class = NewTicketForm
    template_name = 'website/Ticket.html'
    success_url = reverse_lazy('website:ticket_list')
    action='create'


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, ActionContextMixin, UpdateView):
    model = Ticket
    form_class = NewTicketForm
    template_name = 'website/Ticket.html'
    success_url = reverse_lazy('website:ticket_list')
    action='edit'

    def test_func(self):
        ticket = self.get_object()
        return self.request.user == ticket.user

class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, ActionContextMixin, DeleteView):
    model = Ticket
    template_name = 'website/Ticket.html'
    success_url = reverse_lazy('website:ticket_list')
    action='delete'

    def test_func(self):
        ticket = self.get_object()
        return self.request.user == ticket.user

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'website/Ticket.html'

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'website/TicketList.html'
    context_object_name = 'tickets'
    
    def get_queryset(self):
        return Ticket.objects.all()

class ReviewCreateView(LoginRequiredMixin, ActionContextMixin, CreateView):
    action = 'create'
    model = Review
    template_name = 'website/Review.html'
    success_url = reverse_lazy('website:review_list')

    def get_form_class(self):
        if self.request.GET.get('ticket'):
            return ReviewForm
        return CombinedTicketReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.request.GET.get('ticket')
        if ticket_id:
            context['ticket'] = get_object_or_404(Ticket, pk=ticket_id)
        return context

    def form_valid(self, form):
        if isinstance(form, ReviewForm):
            form.instance.user = self.request.user
            form.instance.ticket_id = self.request.GET.get('ticket')
            return super().form_valid(form)
        else:
            # Création du ticket
            ticket = Ticket.objects.create(
                book=form.cleaned_data['ticket_book'],
                description=form.cleaned_data['ticket_description'],
                image=form.cleaned_data['ticket_image'],
                user=self.request.user
            )
            # Création de la review
            review = Review.objects.create(
                headline=form.cleaned_data['headline'],
                rating=form.cleaned_data['rating'],
                body=form.cleaned_data['body'],
                user=self.request.user,
                ticket=ticket
            )
            return redirect(self.success_url)

    def get_initial(self):
        initial = super().get_initial()
        ticket_id = self.request.GET.get('ticket')
        if ticket_id:
            initial['ticket'] = ticket_id
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if not self.request.GET.get('ticket'):
            kwargs.pop('instance', None)
        return kwargs

    def get_form(self, form_class=None):
        form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        
        if issubclass(form_class, ReviewForm):
            form = form_class(**kwargs)
            ticket_id = self.request.GET.get('ticket')
            if ticket_id:
                form.fields['ticket'].widget = forms.HiddenInput()
                form.fields['ticket'].initial = ticket_id
                ticket = get_object_or_404(Ticket, pk=ticket_id)
                form.fields['ticket'].label = f"Critique pour: {ticket.book}"
        else:
            form = form_class(**kwargs)
        
        return form
    
class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, ActionContextMixin, UpdateView):
    """
    Vue pour mettre à jour une critique existante.
    UserPassesTestMixin vérifie que l'utilisateur a le droit de modifier cette critique.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'website/Review.html'
    action='edit'


    def test_func(self):
        """
        Vérifie que l'utilisateur actuel est l'auteur de la critique.
        Cette méthode est appelée par UserPassesTestMixin.
        """
        review = self.get_object()
        return self.request.user == review.user

    def get_form_kwargs(self):
        """
        Ajoute le ticket associé aux kwargs du formulaire.
        """
        kwargs = super().get_form_kwargs()
        kwargs['ticket'] = self.object.ticket
        return kwargs

    def get_success_url(self):
        """
        Définit l'URL de redirection après la mise à jour réussie d'une critique.
        """
        return reverse_lazy('review_detail', kwargs={'pk': self.object.pk})

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, ActionContextMixin, DeleteView):
    """
    Vue pour supprimer une critique.
    UserPassesTestMixin vérifie que l'utilisateur a le droit de supprimer cette critique.
    """
    model = Review
    template_name = 'website/Review.html'
    success_url = reverse_lazy('user_reviews')  # Assurez-vous que cette URL existe
    action='delete'

    def test_func(self):
        """
        Vérifie que l'utilisateur actuel est l'auteur de la critique.
        """
        review = self.get_object()
        return self.request.user == review.user

class ReviewDetailView(LoginRequiredMixin, DetailView):
    """
    Vue pour afficher les détails d'une critique.
    LoginRequiredMixin assure que seuls les utilisateurs connectés peuvent voir les détails.
    """
    model = Review
    template_name = 'website/Review.html'

class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'website/ReviewList.html'
    context_object_name = 'reviews'
    
    def get_queryset(self):
        return Review.objects.all()
    
