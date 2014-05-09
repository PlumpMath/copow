#!python
#  pow app generator
#  Generates the PoW Application.
#  options are:
#   see: python generate_app.py --help


from optparse import OptionParser
import sqlite3, sys, os, datetime
import string
import shutil

import copow.lib.powlib as powlib
#import copow.generate_model as generate_model


def main():
    """ Executes the render methods to generate a conroller and basic
        tests according to the given options """
    parser = OptionParser()
    #mode = MODE_CREATE
    parser.add_option("-n", "--name",
                      action="store",
                      type="string",
                      dest="name",
                      help="set the app name",
                      default="None")
    parser.add_option("-d", "--directory",
                      action="store",
                      type="string",
                      dest="directory",
                      help="app base dir",
                      default="./")
    parser.add_option("-f", "--force",
                      action="store_true",
                      dest="force",
                      help="forces overrides of existing app",
                      default="False")

    (options, args) = parser.parse_args()
    #print options, args
    if options.name == "None":
        if len(args) > 0:
            # if no option flag (like -n) is given, it is assumed that
            # the first argument is the appname. (representing -n arg1)
            options.name = args[0]
        else:
            parser.error(
                "You must at least specify an appname by giving -n <name>."
                )

    appdir = options.directory
    appname = options.name
    force = options.force
    start = None
    end = None
    start = datetime.datetime.now()

    gen_app(appname, appdir, force)

    end = datetime.datetime.now()
    duration = None
    duration = end - start
    print(" -- generated_app in(" + str(duration) + ")")

def copy_file_and_set_appname(filename, appname, odir):
    infile = open(filename)
    instr = infile.read()
    infile.close()
    instr = instr.replace("#APPNAME", appname )  # lint:ok
    opath = os.path.join(odir,filename)
    ofile = open(os.path.normpath(opath, "w"))
    ofile.write(instr)
    ofile.close()
    print(" copied and replaced APPNAME for: %s" % (os.path.normpath(opath)))


def render_db_config(appname, appbase):
    """ Creates the db.cfg file for this application
        and puts it in appname/config/db.cfg"""

    infile = open("./config/db.py")
    instr = infile.read()
    infile.close()
    instr = instr.replace("#APPNAME", appname )  # lint:ok
    ofile = open(os.path.normpath(appbase + "/config/db.py"), "w")
    ofile.write(instr)
    ofile.close()
    print(" written file to: %s" % (os.path.normpath(appbase + "/config/db.py")))


def gen_app(appname, appdir, force=False):
    """ Generates the complete App Filesystem Structure for Non-GAE Apps.
        Filesystem action like file and dir creation, copy fiels etc.
        NO DB action in this function """

    appname = str(appname)
    appname = str.strip(appname)
    appname = str.lower(appname)
    #print " -- generating app:", appname

    print()
    print("------------------------------------------")
    print("| creating the directory structure       |")
    print("------------------------------------------")
    powlib.check_create_dir(appdir + appname)
    appbase = os.path.abspath(os.path.normpath(appdir + "/" + appname + "/"))
    #print appbase
    # defines the subdirs to be created. Form { dir : name, subdir_list, __init__.py : Bool }
    # The subdir_lists have the form [(subdir-name, bool-has-__init__.py), ...]
    subdirs = [
                {"name" : "config", "subdirs": [], "init" : True },
                {"name" : "data", "subdirs" : [], "init" : False},
                {"name" : "lib", "subdirs" : [], "init" : True},
                {"name" : "migrations", "subdirs" : [("schemas", True)], "init" : True},
                {"name" : "models", "subdirs": [("basemodels", True)], "init" : True},
                {"name" : "controllers", "subdirs" :  [], "init" : True},
                {"name" : "public", "subdirs" : [
                            ("img", False),
                            ("img/bs", False),
                            ("ico", False),
                            ("css", False),
                            ("css/bs", False),
                            ("js", False),
                            ("js/bs", False),
                            ("doc", False)], "init"  : False},
                {"name" : "stubs", "subdirs" : [("templates", True)], "init" : True},
                {"name" : "views", "subdirs" : [("layouts", False)], "init" : False},
                {"name" : "test", "subdirs" : [("models", True), ("controllers", True)], "init" : True},
                {"name" : "plugins", "subdirs" : [], "init" : True}
              ]
    # Easy Access and more readable code by naming the offsets ;)
    SUBDIR_NAME = 0
    SUBDIR_HAS_INIT = 1
    for elem in subdirs:
          subdir = os.path.join(appbase, str(elem["name"]))
          powlib.check_create_dir(subdir)
          if elem["init"]:
            powlib.check_create_file(subdir, "__init__.py")
          for subs in elem["subdirs"]:
              new_dir = os.path.join(subdir, str(subs[SUBDIR_NAME]))
              powlib.check_create_dir(new_dir)
              if subs[SUBDIR_HAS_INIT]:
                powlib.check_create_file(new_dir, "__init__.py")

    #
    # copy the files in subdirs. Form ( from, to )
    #
    deep_copy_list = [("config", "config"),
                       ("lib", "lib"),
                       ("stubs", "stubs"),
                       ("migrations", "migrations"),
                       ("migrations/schemas", "migrations/schemas"),
                       ("models", "models"),
                       ("models/basemodels", "models/basemodels"),
                       ("stubs/templates", "stubs/templates"),
                       ("public/doc", "public/doc"),
                       ("public/ico", "public/ico"),
                       ("public/img", "public/img"),
                       ("public/img/bs", "public/img/bs"),
                       ("public/css", "public/css"),
                       ("public/css/bs", "public/css/bs"),
                       ("public/js", "public/js"),
                       ("public/js/bs", "public/js/bs"),
                       ("controllers", "controllers"),
                       ("views", "views"),
                       ("views/layouts", "views/layouts"),
                       ("plugins", "plugins")
                       ]

    print() 
    print("------------------------------------------")
    print("| copying files                          |")
    print("------------------------------------------")
    exclude_patterns = [".pyc", ".pyo", ".DS_STORE"]
    exclude_files = ["db.cfg", "__init__.py"]
    for source_dir, dest_dir in deep_copy_list:
        try:
          for source_file in os.listdir(source_dir):
              fname, fext = os.path.splitext(source_file)
              if not fext in exclude_patterns and not source_file in exclude_files:  # lint:ok
                  powlib.check_copy_file(
                      os.path.join(source_dir, source_file), os.path.join(appbase,dest_dir),
                      #os.path.join(appbase + "/" + dest_dir,source_file),
                      replace=[("#APPNAME",appname)]
                      
                  )
              else:
                  print(" excluded: EXCL", source_file)
                  continue
        except Exception as e:
          print(" Error:    ERR  Errno: #%s file: %s " % (e.errno, e.filename))
          pass

    #
    # copy the generator files
    #
    print() 
    print("------------------------------------------")
    print("| copying the generators                  |")
    print("------------------------------------------")
    powlib.check_copy_file("generate_model.py", appbase, replace=[("#APPNAME",appname)])
    powlib.check_copy_file("do_migrate.py", appbase, replace=[("#APPNAME",appname)])
    powlib.check_copy_file("generate_controller.py", appbase, replace=[("#APPNAME",appname)])
    powlib.check_copy_file("generate_migration.py", appbase, replace=[("#APPNAME",appname)])
    #powlib.check_copy_file("scripts/generate_scaffold.py", appbase)
    #powlib.check_copy_file("scripts/generate_mvc.py", appbase)
    #powlib.check_copy_file("simple_server.py", appbase, replace=[("#APPNAME",appname)])
    powlib.check_copy_file("tornado_server.py", appbase, replace=[("#APPNAME",appname)])
    #powlib.check_copy_file("scripts/pow_router.wsgi", appbase)
    powlib.check_copy_file("pow_console.py", appbase, replace=[("#APPNAME",appname)] )
    powlib.check_copy_file("init_copow_dbs.py", appbase, replace=[("#APPNAME",appname)] )
    #powlib.check_copy_file("scripts/runtests.py", appbase)

    #powlib.replace_string_in_file(
    #    os.path.join(appbase + "/" + "simple_server.py"),
    #    ["#APPNAME", appname]
    #)

    #powlib.replace_string_in_file(
    #   os.path.join(appbase + "/" + "pow_router.wsgi"),
    #    ["#POWAPPNAME", appname]
    #)

    #
    # copy the initial db's
    #
    # NOTHING TO DO FOR MONGODB here

    #
    # initiate the db.cfg file
    #
    print() 
    print("------------------------------------------")
    print("| rendering the DB config file           |")
    print("------------------------------------------")
    render_db_config(appname, appbase )

    #print 
    #print "------------------------------------------"
    #print "| generating the copow models            |"
    #print "------------------------------------------"
    #generate_model.render_model(
    #    modelname="app",
    #    force=False,
    #    comment="System class containing the App Base Informations",
    #    output_path=appname+"/models/")

    #generate_model.render_model(
    #    modelname="version",
    #    force=False,
    #    comment="System class containing the Versions",
    #    output_path=appname+"/models/")

    #print 
    #print "------------------------------------------"
    #print "| generating the copow collections        |"
    #print "------------------------------------------"
    
    print()
    print("------------------------------------------")
    print("| Next steps:                            |")
    print("------------------------------------------")
    apppath = os.path.abspath(os.path.normpath(os.path.join("./",appname)))
    print(" 1. add your app: %s to the PYTHONPATH" % (appname))
    print(r"  -> Windows  : set PYHTONPATH=%PYTHONPATH%;" + "%s" % (apppath))
    print("  -> Unix/Mac : export PYTHONPATH=$PYTHONPATH;%s" % (apppath))
    print(" 2. read first steps on www.pythononwheels.org/copow")
    print(" 3. have fun ;)")
    print("--------------------------------------------------------")
    return


if __name__ == "__main__":
    main()
