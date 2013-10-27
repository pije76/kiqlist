from django import forms
from .models import Goal, GoalComment


class GoalForm(forms.ModelForm):
	error_css_class = "error"

	class Meta:
		model = Goal
		exclude = ("user", "is_done", "tags")


class DoneGoalForm(forms.Form):
	image = forms.ImageField(required=False, label="")
	description = forms.CharField(widget=forms.Textarea, required=False, label="Description", max_length=140)


class GoalCommentForm(forms.ModelForm):
	class Meta:
		model = GoalComment
		exclude = ("user", "goal", "created")


class GoalTagForm(forms.Form):
	tag = forms.CharField(max_length=100)

	def clean_tag(self):
		tag = self.cleaned_data.get("tag")

		if Goal.objects.filter(tags__iregex="[[:<:]](%s)[[:>:]]" % tag, is_done=True).count() == 0:
			error_message = "The tag does not exist."
			self._errors["tag"] = self.error_class([error_message])
			raise forms.ValidationError(error_message)

		return tag
