#
#
# Init copow mamagement collections
# Sounds bigger than it is. (see models/App.py)
# 
# khz 07/2013
# 

import os
import copow.lib.powlib
import copow.lib.db_conn
import copow.config.db.py
import copow.config.config.py

import #APPNAME.models.App

APPNAME = #APPANME

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
    	v = Version()
	    v.set_environment(env)
	    # "short_name"     :      { "type" : "Text" },   
    	# "long_name"      :      { "type" : "Text" },
    	# "path"           :      { "type" : "Text" },
    	# "comment"        :      { "type" : "Text" }
	    #
	    # setting up the app-db
	    # 
	    a = App()
	    a.set_environment(env)	

	   	a.name = "#APPNAME"
	   	a.path = "#APPPATH"
	   	a.lastversion = 0
	   	a.maxversion = 2
	   	a.currentversion = 2

	   	a.save()


