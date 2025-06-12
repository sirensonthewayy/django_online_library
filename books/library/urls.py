from django.urls import path
from .views import BookView, FeedbackView, HomeView

urlpatterns = [
    path('books/<int:pk>/', BookView.as_view(), name='book'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('home/', HomeView.as_view(), name='home'),
]