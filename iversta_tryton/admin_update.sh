#!/bin/sh
echo Copying to docker...
./copy_to_docker.sh
echo Updating Tryton...
docker exec -it -u root iversta-new bash -c "trytond-admin -u iversta_tryton -dev  -c /etc/trytond.conf --logconf /etc/trytond.log.conf -vv -d iversta --dev" | grep -v INFO
echo Restarting docker
docker restart iversta-new
#echo Trying to restart the script
#docker exec -it -u root iversta-new bash 
#/usr/bin/uwsgi --emperor /etc/uwsgi/apps-enabled/iversta-web-app.ini &
#exit


