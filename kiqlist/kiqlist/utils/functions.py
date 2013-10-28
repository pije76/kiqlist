from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.contrib.sites.models import get_current_site
from kiqlist.utils import SessionKeys


def send_noreply_mail(request, template_alias, subject, variables, to):
	context = Context(variables)
	plaintext = get_template("emails/" + template_alias + ".txt").render(context)
	html = get_template("emails/" + template_alias + ".html").render(context)

	if type(to) is not list:
		to = [to]

	current_site = get_current_site(request)
	from_email = "noreply@" + current_site.domain

	message = EmailMultiAlternatives(subject, plaintext, from_email, to)
	message.attach_alternative(html, "text/html")
	message.send()


def profile_processor(request):
	session = request.session
	if SessionKeys.KEY_PROFILE in session:
		return {SessionKeys.KEY_PROFILE: session[SessionKeys.KEY_PROFILE]}
	return {}