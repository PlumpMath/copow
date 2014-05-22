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

import #APPNAME.models.app as app
import #APPNAME.models.version as version

APPNAME = #APPNAME

if __name__ == "__main__":
    print()
    print("------------------------------------------")
    print("| initializing copow DBs                 |")
    print("------------------------------------------")

    environments = ["development", "test", "production"]
    env = environments[0]
    #
    # setting up the version information
    #
    v = version.Version()
    v.environment = env
    v.short_name = "version"
    v.long_name = "51c45aab45fb9f13048dbe2d_version"
    v.comment ="copow version collection"
    v.save()

    v.environment = env
    v.short_name = "app"
    v.long_name = "51c1965714c9b612bc20b95a_app"
    v.comment ="copow app collection"
    v.save()

    # setting up the app-db
    # 
    a = app.App()

    a.name = "#APPNAME"
    a.path = r"#APPPATH"
    a.lastversion = 0
    a.maxversion = 2
    a.currentversion = 2
    a.save()


