#
#
# Init copow mamagement collections
# Sounds bigger than it is. (see models/App.py)
# 
# khz 07/2013
# 

import os
import #APPNAME.lib.powlib
import #APPNAME.lib.db_conn
import #APPNAME.config.db
import #APPNAME.config.settings

import #APPNAME.models.app
import #APPNAME.models.version

APPNAME = #APPNAME

if __name__ == "__main__":
	print
    print "------------------------------------------"
    print "| initializing copow DBs					|"
    print "------------------------------------------"

    environments = ["development", "test", "production"]

    # track the versions and according information for
    # all environments seperately.
    for env in environments:
    	#
    	# setting up the version information
    	#
    	v = version.Version()
	    v.set_environment(env)
	    # "short_name"     :      { "type" : "Text" },   
    	# "long_name"      :      { "type" : "Text" },
    	# "path"           :      { "type" : "Text" },
    	# "comment"        :      { "type" : "Text" }
	    #
	    # setting up the app-db
	    # 
	    a = app.App()
	    a.set_environment(env)	

	   	a.name = "#APPNAME"
	   	a.path = "#APPPATH"
	   	a.lastversion = 0
	   	a.maxversion = 2
	   	a.currentversion = 2

	   	a.save()


