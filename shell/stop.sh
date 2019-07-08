#!/usr/bin/env bash
option=$1
dir=$(dirname "$0")
cd ${dir}
pid=wbmsbt.pid
if [ -e ${pid} ];then
uwsgi --stop ${pid}
rm -rf ${pid}
echo "uwsgi stop..."
fi
uwsgi_pid=`ps aux|grep "wbmsbt"|grep -v "grep"|awk '{print $2}'`
[ -z ${uwsgi_pid} ] && echo "wbmsbt now is not running." || kill -9 ${uwsgi_pid}

cd - >/dev/null 2>&1

