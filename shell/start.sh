#!/usr/bin/env bash

cd $(dirname "$0")

uwsgi -i uwsgi.ini

cd - >/dev/null 2>&1
