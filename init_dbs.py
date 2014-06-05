#
#
# Init copow mamagement collections
# Sounds bigger than it is. (see models/App.py)
# 
# khz 07/2013
# 

import os
import lib.powlib
import lib.db_conn as db_conn
import config.db
import config.settings

import models.app as app
import models.version as version
import models.user as user
import models.copow_log as copow_log

import do_migrate

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
    if APPNAME in conn.database_names():
        if options.force:
            conn.drop_database[APPNAME]
        else:
            print("Database %s exists ..... use init_db.py -f to force dropping and recreating it.")
            sys.exit(0)


    #
    # setting up the version information
    #
    v = version.Version()
    v.environment = env
    v.short_name = "version"
    v.long_name = "51c45aab45fb9f13048dbe2d_version"
    v.comment ="copow version collection"
    v.version = 1
    v.save()

    v.environment = env
    v.short_name = "app"
    v.long_name = "51c1965714c9b612bc20b95a_app"
    v.comment ="copow app collection"
    v.version = 2
    v.save()

    v.environment = env
    v.short_name = "copow_log"
    v.long_name = "5390626945fb9f1d3c184a15_copow_log"
    v.comment ="copow log collextion"
    v.version = 3
    v.save()

    # setting up the app-db
    # 
    a = app.App()
    a.name = "#APPNAME"
    a.path = r"#APPPATH"
    a.lastversion = 0
    a.maxversion = 3
    a.currentversion = 2
    a.save()

    ## setting up the log db with a standard do_migrate
    do_migrate.do_migrate_to_direction("up")

