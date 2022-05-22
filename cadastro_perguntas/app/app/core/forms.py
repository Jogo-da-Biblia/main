from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

from allauth.account.forms import SignupForm, LoginForm
from allauth.account.adapter import DefaultAccountAdapter



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
	phone = forms.CharField(
		label='Whatsapp',
		max_length=11,
		required=True,
	)
	field_order = ['username', 'email', 'password1', 'password2', 'phone']
		
	def __init__(self, *args, **kwargs):
		super(MyCustomSignupForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['placeholder'] = 'username'
		self.fields['username'].widget.attrs.update({'class': 'input__padrao input__email'})

		self.fields['email'].widget.attrs['placeholder'] = 'email'
		self.fields['email'].widget.attrs.update({'class': 'input__padrao input__email'})

		self.fields['password1'].widget.attrs['placeholder'] = 'digite uma senha'
		self.fields['password1'].widget.attrs.update({'class': 'input__padrao input__senha'})

		self.fields['password2'].widget.attrs['placeholder'] = 'confirme a sua senha'
		self.fields['password2'].widget.attrs.update({'class': 'input__padrao input__senha'})

		self.fields['phone'].widget.attrs['placeholder'] = 'Whatsapp'
		self.fields['phone'].widget.attrs.update({'class': 'input__padrao input__senha'})


class CustomAccountAdapter(DefaultAccountAdapter):
	def save_user(self, request, user, form, commit=True):
		data = form.cleaned_data
		user.username = data.get("username")
		user.name = data.get("username")
		user.email = data.get("email")
		user.phone = data.get("phone")
		user.common_group = Group.objects.get(name='colaboradores')
		user.save()
		return user


class MyCustomLoginForm(LoginForm):
	def __init__(self, *args, **kwargs):
		super(MyCustomLoginForm, self).__init__(*args, **kwargs)

		self.fields['login'].widget.attrs['placeholder'] = 'username ou email'
		self.fields['login'].widget.attrs.update({'class': 'input__padrao input__email'})

		self.fields['password'].widget.attrs['placeholder'] = 'senha'
		self.fields['password'].widget.attrs.update({'class': 'input__padrao input__senha'})