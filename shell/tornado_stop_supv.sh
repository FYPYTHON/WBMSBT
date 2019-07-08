#!/usr/bin/env bash
cd $(dirname "$0")
/home/python3/bin/supervisorctl -u root -p 1234 stop all

supervisor_pid=`ps -ef | grep "supervisord" | grep -v "grep" | awk '{print $2}'`
echo "supervisor_pid:" $supervisor_pid

[ -z "${supervisor_pid}" ] && echo "supervisor now is not running." || kill -9 ${supervisor_pid}

tornado_pid=`ps -ef | grep "python3 main_app.py" | grep -v "grep" | awk '{print $2}'`
echo "tornado_pid:" $tornado_pid
[ -z "${tornado_pid}" ] && echo "tornado  now is not running." || kill -9 ${tornado_pid}

cd - >/dev/null 2>&1
