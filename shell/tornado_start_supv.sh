#!/usr/bin/env bash

cd $(dirname "$0")
if [ -e "/tmp/supervisor.sock" ];then
unlink /tmp/supervisor.sock
fi
supervisord -c /usr/local/supervisor/supervisord.conf 
cd - >/dev/null 2>&1
