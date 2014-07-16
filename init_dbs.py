#
#
# Init copow mamagement collections
# Sounds bigger than it is. (see models/App.py)
# 
# khz 07/2013
# 

import os
import sys
import lib.powlib
import lib.db_conn as db_conn
import config.db
import config.settings as settings
import config.db as dbconfig


import models.app as app
import models.version as version
import models.user as user
import models.copow_log as copow_log

import do_migrate
from #APPNAME.models.user import User
import #APPNAME.ext.user_management as umgmt

from optparse import OptionParser

APPNAME = "#APPNAME"

if __name__ == "__main__":
    
    parser = OptionParser()
    
    parser.add_option( "-f", "--force",
                       action="store_true",
                       dest="force",
                       help="forces dropping an existing DB",
                       default=False)


    (options, args) = parser.parse_args()

    print()
    print("------------------------------------------")
    print("| initializing copow DBs                 |")
    print("------------------------------------------")

    environments = ["development", "test", "production"]
    env = environments[0]
    
    # check if db exists and drop it, if its already there
    conn = db_conn.DBConn().get_client()
    dbname = getattr(dbconfig, settings.base["environment"])["database"]
    print("dbnames: ", conn.database_names(), "dbname to create: ", dbname)
    
    if dbname in conn.database_names():
        if options.force:
            print(" Dropping database: ", dbname)
            conn.drop_database(dbname)
            print(" Now recreating Database: ", dbname )
        else:
            print(" ERROR! Database %s exists ....")
            print(" use init_db.py -f to force dropping and recreating it.")
            sys.exit(0)


    #
    # setting up the version information
    #
    v = version.Version()
    v.environment = env
    v.short_name = "version"
    v.long_name = "version_51c45aab45fb9f13048dbe2d"
    v.comment ="copow version collection"
    v.version = 1
    v.create()

    v.environment = env
    v.short_name = "app"
    v.long_name = "app_51c1965714c9b612bc20b95a"
    v.comment ="copow app collection"
    v.version = 2
    v.create()

    v.environment = env
    v.short_name = "copow_log"
    v.long_name = "copow_log_5390626945fb9f1d3c184a15"
    v.comment ="copow log collextion"
    v.version = 3
    v.create()

    v.environment = env
    v.short_name = "user"
    v.long_name = "user_539a229b56031a0d30c6410e"
    v.comment ="copow user collection"
    v.version = 4
    v.create()

    # setting up the app-db
    # 
    a = app.App()
    a.name = "#APPNAME"
    a.path = r"#APPPATH"
    a.lastversion = 0
    a.maxversion = 4
    a.currentversion = 2
    a.save()

    ## setting up the log db with a standard do_migrate
    do_migrate.do_migrate_to_direction("up")
    ## setting up the user colelction with the std do_migrate
    do_migrate.do_migrate_to_direction("up")

    print("creating the admin user. Username: admin, Password: admin")
    u = User()
    u.loginname = "admin"
    u.password = umgmt.set_password("admin")
    u.create()
