-include /home/y/share/yahoo_cfg/buildyblocks/Make.rules

GIT_VERSION = $(shell /home/y/bin/git_auto_version -p master-)

PACKAGE_VERSION = $(shell echo $(GIT_VERSION) | awk -F '.' '{print $$1"."$$2"."$$3"."build_num}' build_num=${BUILD_NUMBER})

COMPONENT_BIM=./component.bim

export CURRENT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

component:
	 yinst_create -t release package.yicf

pr_build_dashboard: component

component_build_dashboard: BB_BIM_FILE=$(COMPONENT_BIM)
component_build_dashboard: component BB_Dist_Push
