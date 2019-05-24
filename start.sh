#! /bin/sh

PATH=/home/y/bin64:/home/y/bin:$PATH
export PATH

dir=`dirname $0`

mkdir -p $dir/logs

ROOT=/home/y/var/curveball_budget_dashboard
python -c "import cherrypy"
if [ $? -eq 1 ]; then
	/home/y/bin/pip install ujson==1.35 pyopenssl==18.0.0 CherryPy==18.1.0 mysql-connector==2.1.6
fi

cd $dir
ps aux | grep brick_app.py | grep -v grep | awk '{print $2}' | xargs kill -9

# patch cherrypy to ignore SIGHUB signal so that it won't exit after auto-deployment
if [ -e /home/y/lib/python3.6/site-packages/cherrypy/process/plugins.py ]
then
	patch -N /home/y/lib/python3.6/site-packages/cherrypy/process/plugins.py < $dir/patch/cherrypy_process_plugins.patch
fi

nohup python $dir/brick_app.py > $dir/logs/app.log 2>&1 &

pid=`ps aux | grep brick_app.py | grep -v grep | awk '{print $2}'`
if [ "$pid" != "" ]
then
	echo "brick_app.py process is running after start"
	break
else
	echo "brick_app.py process is not running after start. Try again"
fi

echo "please check $dir/logs/app.log to confirm the service is started"

