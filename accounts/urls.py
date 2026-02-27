from django.urls import path
from .views import RegisterView, ContactMessageCreateView
app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('contact-us/', ContactMessageCreateView.as_view(), name='contact-us'),
]
