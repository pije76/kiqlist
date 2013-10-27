import json

from django.core.serializers import serialize
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render


def handle_model(data):
	if "display_dict" in dir(data):
		data = data.display_dict()
	else:
		data = json.loads(serialize("json", [data]))[0]
	return data


def handle_iterable(data):
	if len(data) == 0 or "display_dict" in dir(data[0]):
		data = [x.display_dict() for x in data]
	elif isinstance(data, models.query.QuerySet):
		data = json.loads(serialize("json", data))

	return data


def json_view(data=None, error=None):
	if error and type(error) == tuple:
		error_code = error[0]
		error_message = error[1]
	else:
		error_code = 0
		error_message = ""

	if isinstance(data, models.Model):
		data = handle_model(data)
	elif isinstance(data, models.query.QuerySet) or isinstance(data, list):
		data = handle_iterable(data)

	response = {
		"error_code": error_code,
		"error_message": error_message,
		"data": data
	}

	return HttpResponse(json.dumps(response), mimetype="application/json")


def ajax_form_view(request, form_class, callback, template_filename, template_variables=None, instance=None, initial=None, form_kwargs=None):
	kwargs = form_kwargs if form_kwargs else {}

	if instance:
		kwargs["instance"] = instance
	if initial:
		kwargs["initial"] = initial

	if request.method == "POST":
		form = form_class(request.POST, request.FILES, **kwargs)
	else:
		form = form_class(**kwargs)

	if form.is_valid():
		data = callback(form)
		return json_view(data)

	if type(template_variables) != dict:
		template_variables = {}
	template_variables["form"] = form
	template_variables["instance"] = instance

	return render(request, template_filename, template_variables)


def serve_js_templates(request, name):
	return render(request, "js_templates/%s.html" % (name), {})
