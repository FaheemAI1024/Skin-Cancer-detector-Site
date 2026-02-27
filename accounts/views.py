from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import ContactMessage
from .forms import ContactMessageForm
from django.contrib import messages

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login') 

class ContactMessageCreateView(CreateView):
    model = ContactMessage
    form_class = ContactMessageForm
    template_name = 'contact_us.html'
    success_url = reverse_lazy('accounts:contact-us') 

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your message has been sent successfully!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your submission. Please try again.")
        return super().form_invalid(form)