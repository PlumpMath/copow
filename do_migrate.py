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

# Minversion protects the copow collections (app, ver, user, logging)
MINVERSION = 4


def main():
    parser = OptionParser()

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

    parser.add_option("-e", "--erase",
                      action="store",
                      type="string",
                      dest="erase",
                      help="Erases all versions, schemas and migrations to the given version.",
                      default="None")

    (options, args) = parser.parse_args()
    #print options
    

    start = None
    end = None
    start = datetime.datetime.now()

    
    if options.info:
        # only show current version information
        show_info()
    elif options.erase != "None":
        # erase the given version
        erase_version(int(options.version))
    elif options.set_curr_version != "None":
        # only set the current version 
        set_currentversion(options.set_curr_version)
    elif options.direction != "None":
        # migrate into direction
        do_migrate_to_direction(options.direction)
    elif options.version != "None":
        # migrate to version
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
    module = __import__("#APPNAME"+".migrations." + filename, globals(), locals(), [function_name], 0)        
    module = imp.reload(module)
    #schema = reload(schema_module)
    #print(module.__dict__)
    func = module.__dict__[function_name]
    #print("func:")
    #print(func)
    return func


def erase_version(ver):
    """ erase the given version from version collection. Also remove the schema and migration.
        The model file will be renamed to model_erased.py.
    """
    v = version.Version()
    a = app.App()
    a.find_one()

    v_to_erase = v.find_by("version", ver)
    del_one = os.path.abspath(
        os.path.normpath(os.path.join("./migrations", v_to_erase.long_name + ".py"))
    )
    del_two=os.path.abspath(
        os.path.normpath(os.path.join("./migrations/schemas/", v_to_erase.short_name + "_schema.py"))
    )
    print("  deleting: ", del_one)
    os.remove(del_one)
    print("  deleting: ", del_two)
    os.remove(del_two)
    ren_one = path.abspath(
        os.path.normpath(os.path.join("./models/", v_to_erase.short_name + ".py"))
    )
    ren_two=path.abspath(
        os.path.normpath(os.path.join("./models/", "erased_" + v_to_erase.short_name + ".py"))
    )
    print("  renaming: ", ren_one, " to: ", ren_two)
    os.rename(ren_one, ren_two)

def do_migrate_to_direction(to_direction):
    #powlib.load_module("App")
    if to_direction not in ["up", "down"]:
        raise Exception("Wrong direction given. Only up or down are supported. No left or right ;)")
        sys.exit()

    v = version.Version()
    a = app.App()
    a.find_one()

    print(" ...migrating ")
    #print(a)
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
        if a.currentversion > MINVERSION:
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
    v = version.Version()
    a = app.App()
    a.find_one()
    if to_version >= MINVERSION and to_version <= a.maxversion:
        print("..migrating --> to version: %s" % (to_version))
        direction = "None"
        if to_version < a.currentversion:
            times = a.currentversion - to_version
            direction = "down"
        else:
            times = to_version - a.currentversion
            direction = "up"
        for runs in range(0,times):
            do_migrate_to_direction(direction)

    else:
        print("  -- cannot migrate above maxversion: ", str(a.maxversion), " or MINVERSION: ", str(MINVERSION))
    

    return


def set_currentversion(ver):
    print("  migrating ")
    v = version.Version()
    a = app.App()
    a.find_one()

    if ver <= a.maxversion and ver > MINVERSION:
        # set the given version
        a.currentversion = ver
    else:
        print("  -- cannot migrate above maxversion: ", str(a.maxversion), " or MINVERSION: ", str(MINVERSION))

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
        print(type(elem))
        print(elem)




if __name__ == '__main__':
    main()
