#! /bin/sh

dir=`dirname $0`

mkdir -p $dir/logs

ps aux | grep brick_app.py | awk '{print $2}' | xargs kill -9
cd $dir && python $dir/brick_app.py > $dir/logs/app.log 2>&1 &
echo "please check $dir/logs/app.log to confirm the service is started"
