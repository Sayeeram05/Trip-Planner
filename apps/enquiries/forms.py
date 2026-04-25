from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = [
            "full_name",
            "phone",
            "email",
            "location",
            "destination",
            "travel_date",
            "people_count",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your full name",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+91 XXXXX XXXXX",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "your@email.com",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "City, State where you live",
                }
            ),
            "destination": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": "readonly",
                }
            ),
            "travel_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "people_count": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "Number of travellers",
                }
            ),
        }
        labels = {
            "full_name": "Full Name",
            "phone": "Phone Number",
            "email": "Email Address",
            "location": "Your Location",
            "destination": "Destination",
            "travel_date": "Travel Date",
            "people_count": "Number of People",
        }
