from django.forms import ModelForm
from .models import Status


class StatusForm(ModelForm):
	error_css_class = "error"

	class Meta:
		model = Status
		exclude = ("created", "user", "tags")
