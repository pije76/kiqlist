from django import forms
from django.contrib.auth.models import User
from models import PrivateMessage


class PrivateMessageForm(forms.ModelForm):
	class Meta:
		model = PrivateMessage
		exclude = ("from_user", )


class StartConversationForm(forms.Form):
	username = forms.CharField(max_length=255)

	def clean_username(self):
		username = self.cleaned_data.get("username")

		try:
			self.user = User.objects.get(username=username)
		except User.DoesNotExist:
			error_message = "No user was found with the specified username."
			self._errors["username"] = self.error_class([error_message])
			raise forms.ValidationError(error_message)

		return username
