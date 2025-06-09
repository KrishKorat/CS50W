from django import forms
from .models import Listing

CATEGORY_CHOICES = [
    ('', 'Select Category'),
    ('Fashion', 'Fashion'),
    ('Toys', 'Toys'),
    ('Electronics', 'Electronics'),
    ('Home', 'Home'),
    ('Books', 'Books'),
    ('Others', 'Others'),
]

class ListingForm(forms.ModelForm):
  category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)

  class Meta:
    model = Listing
    fields = ["title", "description", "starting_bid", "image_url", "category"]
