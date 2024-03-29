from fabric.api import *
from fabric.contrib.console import confirm

env.use_ssh_config = True
env.roledefs = {'web': ['rapback_web'], 'celery': ['rapback_celery']}
code_dir = "~/rapback"

@roles('web')
def test():
    with settings(warn_only=True):
        result = local('python manage.py test rapback')
    if result.failed and not confirm("Test failed. Continue anyway?"):
        abort("Aborting at user request.")

@roles('web')
def commit(message):
    local('''git add -p && git commit -m %s''' % message)

@roles('web')
def push():
    local('git push origin')

@roles('web')
def merge_to_master(branch_name):
    local('git checkout master && git merge ' + branch_name)

@roles('web')
def prepare_deploy(message):
    print message
    commit(message)
    push()

@roles('web', 'celery')
def deploy():
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git@github.com:mlp5ab/RapbackWeb.git %s" % code_dir)
            with cd(code_dir):
                run('source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv rapback')
                run("workon rapback && pip install -r requirements.txt")
    with cd(code_dir):
        run("git pull origin")
        # run("workon rapback && python manage.py migrate")

@roles('web', 'celery')
def full_deploy(message):
    prepare_deploy(message)
    deploy()

@roles('web')
def migrate():
    with cd(code_dir):
        run("workon rapback && python manage.py migrate")

@roles('web')
def run_debug():
    with cd(code_dir):
        run("python manage.py runserver 0.0.0.0:8000")

@roles('celery')
def restart_celery():
    run("workon rapback && supervisorctl -c ~/.supervisor/supervisord.conf restart rapback-celery")

@roles('web')
def restart_web():
    run("workon rapback && supervisorctl -c .supervisor/supervisord.conf restart rapback-web")

def append_keys():
    for key in []:
        run("echo {} >> ~/.bashrc".format(key))
    run("source ~/.bashrc")

# def setup_new_aws_instance():
#     with cd("~"):
#         run('wget https://bootstrap.pypa.io/get-pip.py')
#         run('sudo python get-pip.py')
#         run('sudo pip install virtualenv')
#         run('sudo pip install virtualenvwrapper')
#         run('echo WORKON_HOME=$HOME/.virtualenvs >> .bashrc')
#         run('echo source /usr/bin/virtualenvwrapper.sh >> .bashrc')
#         run('source .bashrc')
#         run('mkvirtualenv rapback -p /usr/bin/python2.7')
#         run('sudo yum install git')
#         run('sudo yum install gcc python-setuptools python-devel postgresql-devel')
#     deploy()
#     with cd(code_dir):
#         run('workon rapback && pip install -r requirements.txt')


# def setup_new_instance():
#     with cd("~"):
#         run('sudo apt-get update')
#         run('sudo apt-get upgrade')
#         run('wget https://bootstrap.pypa.io/get-pip.py')
#         run('sudo python get-pip.py')
#         run('sudo pip install virtualenv')
#         run('sudo pip install virtualenvwrapper')
#         run('echo WORKON_HOME=$HOME/.virtualenvs >> .bashrc')
#         run('echo source /usr/local/bin/virtualenvwrapper.sh >> .bashrc')
#         run('source .bashrc')
#         run('sudo apt-get install git-core gcc libpq-dev python-dev postgresql postgresql-contrib python-setuptools nginx')
#     deploy()
#     with cd(code_dir):
#         run('workon rapback && pip install -r requirements.txt')


def setup_new_instance():
    with cd("~"):
        run('sudo apt-get update')
        run('sudo apt-get install gcc postgresql postgresql-contrib libpq-dev python-dev python-setuptools nginx build-essential git')
        run('sudo apt-get install python3 python3-dev')
        run('sudo apt-get install python-pip')
        run('sudo pip install virtualenv virtualenvwrapper')
        run('echo export WORKON_HOME=$HOME/.virtualenvs >> .bashrc')
        run('echo export PROJECT_HOME=$HOME>>.bashrc')
        run('echo source /usr/local/bin/virtualenvwrapper.sh>>.bashrc')
        run('source .bashrc')
        run('mkvirtualenv rapback')
    print "You now need to ssh in to create a ssh key... Also you still need to add awscreds."