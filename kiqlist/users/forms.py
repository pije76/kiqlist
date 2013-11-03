from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
	error_css_class = "error"

	username = forms.CharField(max_length=100, label="Username")
	password = forms.CharField(max_length=100, label="Password")
	user = None

	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		username = cleaned_data.get("username")
		password = cleaned_data.get("password")

		if username and password:
			self.user = authenticate(username=username, password=password)

			if self.user is None:
				error_message = "Username or password is incorrect."
				self._errors["username"] = self.error_class([error_message])
				self._errors["password"] = self.error_class([error_message])
				raise forms.ValidationError(error_message)
			elif not self.user.is_active:
				raise forms.ValidationError("User is not currently activated.")

		return cleaned_data


class RegisterForm(forms.Form):
	error_css_class = "error"

	first_name = forms.CharField(max_length=100, label="First name")
	last_name = forms.CharField(max_length=100, label="Last name")
	username = forms.CharField(max_length=100, label="Username")
	email = forms.EmailField(label="E-mail")
	password = forms.CharField(max_length=100, label="Password")
	password_confirmation = forms.CharField(max_length=100, label="Confirm password")

	def clean(self):
		cleaned_data = super(RegisterForm, self).clean()
		username = cleaned_data.get("username")
		email = cleaned_data.get("email")
		password = cleaned_data.get("password")
		password_confirmation = cleaned_data.get("password_confirmation")

		if password and password_confirmation and password != password_confirmation:
			error_message = "Password does not match the confirm password."
			self._errors["password"] = self.error_class([error_message])
			self._errors["password_confirmation"] = self.error_class([error_message])
			raise forms.ValidationError(error_message)

		if User.objects.filter(username=username).exists():
			error_message = "Username is already exists."
			self._errors["username"] = self.error_class([error_message])
			raise forms.ValidationError(error_message)

		if User.objects.filter(email=email).exists():
			error_message = "E-mail is already exists."
			self._errors["email"] = self.error_class([error_message])
			raise forms.ValidationError(error_message)

		return cleaned_data


class ProfileForm(forms.Form):
	error_css_class = "error"

	first_name = forms.CharField(max_length=100, label="First name")
	last_name = forms.CharField(max_length=100, label="Last name")
	email = forms.EmailField(label="E-mail")
	about = forms.CharField(max_length=255, label="About", required=False)
	location = forms.CharField(max_length=255, label="Location", required=False)


class ChangePasswordForm(forms.Form):
	current_password = forms.CharField(max_length=100, label="Current password")
	password = forms.CharField(max_length=100, label="Password")
	password_confirmation = forms.CharField(max_length=100, label="Password confirmation")

	def __init__(self, *args, **kwargs):
		self.user = kwargs["user"]
		del kwargs["user"]

		super(ChangePasswordForm, self).__init__(*args, **kwargs)

	def clean_current_password(self):
		current_password = self.cleaned_data.get("current_password")

		if not self.user.check_password(current_password):
			error_message = "Current password is incorrect."
			self._errors["current_password"] = self.error_class([error_message])
			raise forms.ValidationError(error_message)

		return current_password

	def clean_password_confirmation(self):
		password = self.cleaned_data.get("password")
		password_confirmation = self.cleaned_data.get("password_confirmation")

		if not password or not password_confirmation or password != password_confirmation:
			error_message = "The two password fields didn't match."
			self._errors["password"] = self.error_class([error_message])
			self._errors["password_confirmation"] = self.error_class([error_message])
			raise forms.ValidationError(error_message)


class ProfilePhotoForm(forms.Form):
	photo = forms.ImageField(required=False)
	delete = forms.BooleanField(label="Delete photo", required=False)
