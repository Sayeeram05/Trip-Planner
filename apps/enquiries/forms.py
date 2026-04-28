from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    def clean_travel_date(self):
        travel_date = self.cleaned_data.get("travel_date")
        if travel_date and travel_date < date.today():
            raise ValidationError("Travel date must be in the future.")
        return travel_date

    def clean_people_count(self):
        count = self.cleaned_data.get("people_count")
        if count and (count < 1 or count > 50):
            raise ValidationError("Enter a valid number of people (1-50).")
        return count

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
