from django import forms
from kiqlist.hash_tags.models import HashTag


class HashTagForm(forms.Form):
	tag = forms.CharField(max_length=100)

	def clean_tag(self):
		tag = self.cleaned_data.get("tag")

		if HashTag.objects.filter(title=tag).count() == 0:
			error_message = "The tag does not exist."
			self._errors["tag"] = self.error_class([error_message])
			raise forms.ValidationError(error_message)

		return tag