command="$@"

source /etc/bashrc

HIVE_QUEUE=curveball_med
HIVE="/home/y/bin/hive -hiveconf mapred.job.queue.name=$HIVE_QUEUE -e "

export HDFS_HOME=/home/y/share/hadoop
export HIVE_HOME=/home/y/libexec/hive
export JAVA_HOME=/home/y/libexec64/java
export HDFS_COMMON_LIB_NATIVE_DIR=$HDFS_HOME/lib/native
export HDFS_OPTS="$HDFS_OPTS -Djava.library.path=$HDFS_HOME/lib"
export PATH=$PATH:$HDFS_HOME/bin:$JAVA_HOME/bin:$HIVE_HOME/bin
export LD_LIBRARY_PATH=$HDFS_HOME/lib/native/:$LD_LIBRARY_PATH

kinit -k -t /home/bud_prd/bud_prd.prod.headless.keytab bud_prd@YGRID.YAHOO.COM

$HIVE "$command"

exit 0;