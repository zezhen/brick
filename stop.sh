#! /bin/sh

PATH=/home/y/bin64:/home/y/bin:$PATH
export PATH

ps aux | grep app.py | grep -v grep | awk '{print $2}' | xargs kill -9 || true
