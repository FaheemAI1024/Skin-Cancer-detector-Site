from django import forms
from .models import ContactMessage
from django.core.exceptions import ValidationError
import re

class ContactMessageForm(forms.ModelForm):
    # Custom fields and form-level validations
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name',
            'aria-label': 'Your name',
        }),
        label='Full Name',
        help_text="Please enter your full name.",
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address',
            'aria-label': 'Your email',
        }),
        label='Email Address',
        help_text="We will never share your email with anyone else.",
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message',
            'rows': 5,
            'aria-label': 'Your message',
        }),
        label='Your Message',
        max_length=500,  # Limit the message length
        help_text="Your message cannot be longer than 500 characters.",
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

    # Optional: Add custom labels and error messages
    labels = {
        'name': 'Your Full Name',
        'email': 'Your Email Address',
        'message': 'Your Message',
    }

    error_messages = {
        'name': {
            'required': 'Your name is required.',
            'max_length': 'Name cannot be longer than 100 characters.',
        },
        'email': {
            'required': 'Please provide a valid email address.',
            'invalid': 'Enter a valid email address.',
        },
        'message': {
            'required': 'Please enter a message.',
            'max_length': 'Message too long (maximum 500 characters).',
        },
    }

    # You can add custom validators if needed (for example, for message content)
    def clean_message(self):
        message = self.cleaned_data.get('message')
        # You can add further validation or filtering here
        return message
