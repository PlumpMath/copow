3#!python
# do_migrate
# execute db migrations and jobs.
# also modify migrations (erase, set version etc)
#
#

import os
from optparse import OptionParser
import sys
import datetime
import imp
from #APPNAME.models import app
from #APPNAME.models import version

import #APPNAME.lib.powlib as powlib
import #APPNAME.config.settings as settings 

# setting the right defaults
MODE_CREATE = 1
MODE_REMOVE = 0


def main():
    parser = OptionParser()
    mode = MODE_CREATE

    parser.add_option("-d", "--direction",
                      action="store",
                      type="string",
                      dest="direction",
                      help="migrate [up | down]",
                      default="None")
    parser.add_option("-v", "--version",
                      action="store",
                      type="string",
                      dest="version",
                      help="migrates to version ver",
                      default="None")
    #parser.add_option("-e", "--erase",
    #                  action="store_true",
    #                  dest="erase",
    #                  help="erases version ver",
    #                  default="False")
    parser.add_option("-i", "--info",
                      action="store_true",
                      dest="info",
                      help="shows migration information",
                      default=False)
    
    parser.add_option("-s", "--set-currentversion",
                      action="store",
                      type="string",
                      dest="set_curr_version",
                      help="sets cuurentversion to given version ver",
                      default="None")

    (options, args) = parser.parse_args()
    #print options
    

    start = None
    end = None
    start = datetime.datetime.now()

    # only show current version information
    if options.info:
        show_info()
    # only set the current version 
    elif options.set_curr_version != "None":
        set_currentversion(options.set_curr_version)
    # migrate into direction
    elif options.direction != "None":
        do_migrate_to_direction(options.direction)
    # migrate to version
    elif options.version != "None":
        ver = int(options.version)
        do_migrate_to_version(ver)

    else:
        #Error
        print("You must give a valid option to do_migrate. See do_migrate.py --help ")
        sys.exit()

    end = datetime.datetime.now()
    duration = None
    duration = end - start
    print("migrated in(" + str(duration) + ")")

def load_func( filename, function_name):
    print("  Trying to load: ", filename, " -> ", function_name)
    module = __import__("atest"+".migrations." + filename, globals(), locals(), [function_name], 0)        
    module = imp.reload(module)
    #schema = reload(schema_module)
    #print(module.__dict__)
    func = module.__dict__[function_name]
    #print("func:")
    #print(func)
    return func

def do_migrate_to_direction(to_direction):
    #powlib.load_module("App")
    if to_direction not in ["up", "down"]:
        raise Exception("Wrong direction given. Only up or down are supported. No left or right ;)")
        sys.exit()

    v = version.Version()
    a = app.App()
    a.find_one()

    print(" ...migrating ")
    if to_direction == "up":
        # check if current_version == maxversion => Error. Cannot migrate higher than max.
        if a.currentversion < a.maxversion:
            # ok, migrating up
            to_version = a.currentversion + 1
            v = v.find_one({ "version" :  to_version })
            print("-"*50)
            print("  Trying to migrate to this version now: ", str(to_version))
            print("-"*50)
            print(v)
            up = load_func(v.long_name, "up")
            #execute the up() function
            up()
            a.currentversion = to_version
            a.update()
        else:
            raise Exception("Cannot migrate up. You are already on maxversion")
    elif to_direction == "down":
        # check if currentversion > 2 :
        if a.currentversion > 2:
            # ok, migrate down
            to_version = a.currentversion - 1
            v = v.find_one({ "version" :  a.currentversion })
            print("  Trying to migrate to this version now: ", str(to_version))
            print("-"*40)
            down = load_func(v.long_name, "down")
            #execute the up() function
            down()
            a.currentversion = to_version
            a.update()
        else:
            # not ok, bailing out.
            raise Exception(
                "Cannot migrate down below version 2, since version 1 and 2 represent copow system collections")
      

def do_migrate_to_version(to_version):
    #powlib.load_module("App")
    print("..migrating ")
    print("    -- to version: %s" % (to_version))
    

    return


def set_currentversion(ver):
    print("migrating ")
    return


def show_info():
    a = app.App()
    a = a.find_one()
    print("showing migration information for")
    #print " -- Appname: " + app.name
    print(" -- currentversion is : " + str(a.currentversion))
    print(" -- max version is : " + str(a.maxversion))
    print("listing all versions:")
    print("-"*50)
    v = version.Version()
    version_list = v.find_all()
    for elem in version_list:
        print(elem)




if __name__ == '__main__':
    main()
