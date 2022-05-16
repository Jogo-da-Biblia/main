from logging import PlaceHolder
from tabnanny import verbose
from turtle import textinput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

from allauth.account.forms import SignupForm


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class MyCustomSignupForm(SignupForm):
	field_order = ['username', 'email', 'password1', 'password2', 'phone']
	phone = forms.CharField(
		label='Whatsapp',
		max_length=11,
		required=True,
	)

	def save(self, request):
		user = super(MyCustomSignupForm, self).save(request)
		user.name = self.cleaned_data['username']
		user.phone = self.cleaned_data['phone']
		user.common_group = Group.objects.get(name='colaboradores')
		user.save()
		return user
		
	def __init__(self, *args, **kwargs):
		super(MyCustomSignupForm, self).__init__(*args, **kwargs)
		self.fields['phone'].widget.attrs['placeholder'] = 'Whatsapp'

		self.fields['phone'].widget.attrs.update({'class': 'form-control-lg'})
