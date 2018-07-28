#!/bin/bash
pkill -9 uwsgi
echo "----------------------------------------------------------------------------"
nohup uwsgi --ini hello_django_uwsgi.ini &
echo '****************************************************************************'
service nginx restart
