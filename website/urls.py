from django.urls import path
from .views import (
    HomeView,
    ReviewCreateView, ReviewUpdateView, ReviewDeleteView, ReviewDetailView, ReviewListView,
    TicketCreateView, TicketUpdateView, TicketDeleteView, TicketDetailView, TicketListView,
    UserProfileView, SubscribeView, UnsubscribeView, FollowedUsersView
)

app_name = 'website'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('followed-users/', FollowedUsersView.as_view(), name='followed_users'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('subscribe/<str:username>/', SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/<str:username>/', UnsubscribeView.as_view(), name='unsubscribe'),   
    # Routes pour les opérations CRUD sur les critiques
    path('review/create/', ReviewCreateView.as_view(), name='create_review'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('review/<int:pk>/edit/', ReviewUpdateView.as_view(), name='edit_review'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='delete_review'),
    path('reviews/', ReviewListView.as_view(), name='review_list'),
   
    # Routes pour les opérations CRUD sur les tickets
    path('ticket/create/', TicketCreateView.as_view(), name='create_ticket'),
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('ticket/<int:pk>/edit/', TicketUpdateView.as_view(), name='edit_ticket'),
    path('ticket/<int:pk>/delete/', TicketDeleteView.as_view(), name='delete_ticket'),
    path('tickets/', TicketListView.as_view(), name='ticket_list'),
]