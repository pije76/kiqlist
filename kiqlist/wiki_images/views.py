import json
import urllib2
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings


def get_list(request):
	query = request.GET.get("query", None)
	if not query:
		return HttpResponse()

	response = urllib2.urlopen(settings.WIKI_IMAGES_LIST_URL % urllib2.quote(query))
	data = json.loads(response.read())

	images_titles = []
	for page in data["query"]["pages"].values():
		if "images" in page:
			for image in page["images"]:
				images_titles.append(image["title"])

	def is_right_ext(image):
		return len(filter(None, [image.lower().endswith(y) for y in settings.WIKI_IMAGES_EXT])) > 0

	images_titles = filter(is_right_ext, images_titles)
	images_titles = images_titles[:settings.WIKI_IMAGES_LIMIT]

	images = []
	for image_title in images_titles:
		response = urllib2.urlopen(settings.WIKI_IMAGE_INFO_URL % urllib2.quote(image_title.encode("utf-8")))
		data = json.loads(response.read())
		for page in data["query"]["pages"].values():
			for image in page["imageinfo"]:
				images.append({
					"url": image["url"],
					"thumburl": image["thumburl"]
				})

	return render(request, "wiki_images/list.html", {
		"images": images
	})
