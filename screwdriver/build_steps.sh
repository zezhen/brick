# import common functions 
. /home/y/bin/cbsd_common_steps.sh

function pr_build()
{
    gmake -f Makefile pr_build_dashboard
}

function component_build()
{
    gmake -f Makefile component_build_dashboard
}
