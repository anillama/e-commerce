from django import forms
from .models import Auction

class CreateAuction(forms.ModelForm):
	class Meta:
		model = Auction
		fields = ['title', 'discription', 'price', 'category', 'image']

		widgets = {
			'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Title'}),
			'discription' : forms.Textarea(attrs={'class': 'form-control','placeholder':'Discription'}),
			'price' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Price'}),
			'category' : forms.Select(attrs={'class': 'form-control'})

		}