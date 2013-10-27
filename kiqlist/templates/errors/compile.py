#!/usr/bin/env python

import os
from django.conf import settings
from django.template.loader import render_to_string

ERRORS = {
	400: ("Bad Request",
		"Your client has issued a malformed or illegal request."),

	403: ("Forbidden",
		"You don't have permission to access this resource."),

	404: ("Not Found",
		"The requested URL was not found on this server."),

	405: ("Method Not Allowed",
		"The request method is not supported by this resource."),

	410: ("Gone",
		"This resource is no longer available."),

	414: ("Request-URI Too Long",
		"The requested URL is too large to process."),

	500: ("Internal Server Error",
		"The server encountered an error and could not complete your request."),

	502: ("Bad Gateway",
		"The gateway received an invalid response from the upstream server."),

	503: ("Service Unavailable",
		"The server is currently unavailable."),

	504: ("Gateway Timeout",
		"The request to the upstream server timed out."),
}

def main():
	settings.configure(TEMPLATE_DIRS=[os.path.dirname(os.path.abspath(__file__))])
	for code, t in ERRORS.items():
		name, desc = t
		out = render_to_string("error.html", {"error_code": code, "error_name": name, "error_desc": desc})

		filename = "%i.html" % (code)
		print("Compiling %s" % (filename))
		with open(filename, "w") as f:
			out = out.replace("\t", "").replace("\n", "")
			f.write(out)

if __name__ == "__main__":
	main()
