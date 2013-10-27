"""
Fabfile for Fabric to run
Deploy with:
	$ fab deploy

Create a new environment with:
 # adduser --system --home /home/git --shell /usr/bin/git-shell --group  git
 # cd ~git
 # git init --bare $PROJECT.git
 # chown -R git:git .
"""

from fabric.api import *

PROJECT = "kiqlist"
PORT = 80

env.hosts = ["176.58.110.56"]
env.user = "root"
env.shell = "/bin/zsh -c"
env.scss = "/var/lib/gems/1.8/bin/scss"
env.deploy_user = "www-data"
env.directory = "/var/www/%s/%s" % (PROJECT, PROJECT)
env.activate = "source %s/../env.%s/bin/activate" % (env.directory, PROJECT)

def install_requirements():
	with prefix(env.activate):
		pull()
		run("pip install -r %s/requirements.txt" % (env.directory))

def compile_scripts():
	with cd("static/js"):
		sudo("java -jar /usr/lib/jvm/compiler.jar --js "
			"main.js "
			"--js_output_file global.min.js", user=env.deploy_user)

def pull():
	with cd(env.directory):
		sudo("git pull", user=env.deploy_user)

def prepare():
	with cd(env.directory):
		run("cp ../%s_settings.py %s/local_settings.py" % ("live", PROJECT))
		pull()
		run("python ./manage.py syncdb")
		with cd(PROJECT):
			sudo("python templates/errors/compile.py", user=env.deploy_user)
			sudo("%s static/css/main.scss static/css/global.css --style=compressed" % (env.scss), user=env.deploy_user)
			# compile_scripts()

def stop_services():
	with settings(warn_only=True):
		sudo("service nginx stop")
		sudo("killall -9 python gunicorn gunicorn_django")

def start_services():
	with cd(env.directory):
		if False:
			sudo("python ./manage.py runserver 0.0.0.0:%i" % (PORT))
		else:
			sudo("gunicorn_django "
				"--user %(user)s "
				"--group %(user)s "
				#"--access-logfile %(dir)s/../log/gunicorn.access.log "
				"--error-logfile %(dir)s/../log/gunicorn.error.log "
				"--workers=4 "
				"--worker-class=egg:gunicorn#sync "
				"--timeout=30 "
				"-b 127.0.0.1:8000 -D" % {"user": env.deploy_user, "dir": env.directory},
			user=env.deploy_user)
			sudo("service nginx start")

def deploy():
	with prefix(env.activate):
		prepare()
		stop_services()
		start_services()
