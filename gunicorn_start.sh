#!/bin/sh
set -e
LOGFILE=/var/log/gunicorn/rapback.log
ERRFILE=/var/log/gunicorn/rapback.err
LOGDIR=$(dirname $LOGFILE)
ERRDIR=$(dirname $ERRFILE)
NUM_WORKERS=3
USER=ubuntu
DJANGO_WSGI_MODULE=rapback.wsgi
cd /home/ubuntu/rapback
source /usr/local/bin/virtualenvwrapper.sh
workon rapback
test -d $LOGDIR || mkdir -p $LOGDIR
test -d $ERRDIR || mkdir -p $ERRDIR
exec gunicorn --error-logfile=$ERRFILE --log-file=$LOGFILE \
                -w $NUM_WORKERS -b 0.0.0.0:8000 ${DJANGO_WSGI_MODULE}:application




#NAME="rapback" # Name of the application
#DJANGODIR=/home/vagrant/projects/rapback # Django project directory
#SOCKFILE=/home/vagrant/projects/gunicorn.sock # we will communicte using this unix socket
#USER=vagrant # the user to run as
#NUM_WORKERS=2 # how many worker processes should Gunicorn spawn
#DJANGO_SETTINGS_MODULE=rapback.settings # which settings file should Django use
#DJANGO_WSGI_MODULE=rapback.wsgi # WSGI module name
#
#echo "Starting $NAME as `whoami`"
#
## Activate the virtual environment
#cd $DJANGODIR
#export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
#export PYTHONPATH=$DJANGODIR:$PYTHONPATH
#
## Create the run directory if it doesn't exist
#RUNDIR=$(dirname $SOCKFILE)
#test -d $RUNDIR || mkdir -p $RUNDIR
#
## Start your Django Unicorn
## Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
#echo "about to exec exec is" $DJANGO_WSGI_MODULE
#exec gunicorn ${DJANGO_WSGI_MODULE}:application \
#--name $NAME \
#--workers $NUM_WORKERS \
#--user=$USER \
#--log-level=debug \
#--bind=unix:$SOCKFILE