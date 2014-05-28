#!python
# do_migrate
# execute db migrations and jobs.
# also modify migrations (erase, set version etc)
#
#

import os
from optparse import OptionParser
import sys
import datetime


#sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))  # lint:ok
#sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./models" )))  # lint:ok
#sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./controllers" )))  # lint:ok
#sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./migrations" )))  # lint:ok


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
                      default="False")
    
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



def do_migrate_to_direction(to_direction):
    #powlib.load_module("App")
    
    if to_direction not in ["up", "down"]:
        print("ERROR: unknown direction: %s" % (to_direction))
        sys.exit()

    v = version.Version()
    a = app.App()

    print("..migrating ")
    if to_direction == "up":
        # check if current_version == maxversion => Error. Cannot migrate higher than max.
        if a.currentversion == a.maxversion:
            print("ERROR: cannot migrate higher that max.")
            sys.exit()
        else:
            
            print("    -- Up: %s" % (to_direction))

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
    v = version.Version()
    version_list = v.find_all()
    for elem in version_list:
        print elem




if __name__ == '__main__':
    main()
