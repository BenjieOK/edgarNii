from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["full_name", "email", "subject", "message"]
        labels = {
            "full_name": "Full Name",
            "email": "Email Address",
            "subject": "Subject",
            "message": "Message",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "your@email.com"}),
            "subject": forms.TextInput(attrs={"placeholder": "Subject"}),
            "message": forms.Textarea(attrs={"rows": 6, "placeholder": "Your message..."}),
        }
