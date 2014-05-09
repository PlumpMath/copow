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

import #APPNAME.lib.powlib
from #APPNAME.models import App
from #APPNAME.lib.pow_objects import PowTable

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
                      help="migrate up or down",
                      default="None")
    parser.add_option("-v", "--version",
                      action="store",
                      type="string",
                      dest="version",
                      help="migrates to version ver",
                      default="None")
    parser.add_option("-e", "--erase",
                      action="store_true",
                      dest="erase",
                      help="erases version ver",
                      default="False")
    parser.add_option("-i", "--info",
                      action="store_true",
                      dest="info",
                      help="shows migration information",
                      default="False")
    parser.add_option("-j", "--job",
                      action="store",
                      type="string", dest="job",
                      help="executes a migration job",
                      default="None")
    parser.add_option("-m", "--method",
                      action="store", type="string",
                      dest="method",
                      help="execute the given method. Only in with -j",
                      default="None")
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

    if options.info:
        show_info()
        return

    if options.version == "None":
        ver = None
    else:
        ver = int(options.version)

    if options.erase:
        if not ver:
            print "You must give a version to erase with -v"
            return
        else:
            do_erase(ver)

    if options.job != "None":
        # execute a migration job:
        do_job(options.job, options.method)

    if options.set_curr_version != "None":
        # set the current version 
        set_currentversion(options.set_curr_version)

    # nothing else to do, so do_migrate
    do_migrate(options.direction, options.version)

    end = datetime.datetime.now()
    duration = None
    duration = end - start
    print "migrated in(" + str(duration) + ")"


def do_job(options, filename, method):
    print "migrating"
    return


def do_migrate(to_version, direction):
    #powlib.load_module("App")
    print "..migrating "
    print "    -- to version: %s" % (to_version)
    

    return


def set_currentversion(ver):
    print "migrating "
    return


def do_erase():
    return


def show_info():
    print "showing migration information for"
    #print " -- Appname: " + app.name
    print " -- currentversion is : " + str(app.currentversion)
    print " -- max version is : " + str(app.maxversion)




if __name__ == '__main__':
    main()
