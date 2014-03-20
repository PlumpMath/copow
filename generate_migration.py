#!python
#  pow migration generator.
#
# options are: 
#   see: python generate_migration.py --help


import os
import time
from optparse import OptionParser
import sys
import datetime
import string

from #APPNAME.models import App

import copow.lib.powlib
from copow.config import config
from bson.objectid import ObjectId

PARTS_DIR = config.base["parts_dir"]

    
def main():
    """ Executes the render methods to generate a migration according to the given options """
    parser = OptionParser()
    
    parser.add_option( "-m", "--model",  
                       action="store", 
                       type="string", 
                       dest="model", 
                       help="defines the model for this migration.", 
                       default ="None")
    parser.add_option( "-c", "--comment",  
                       action="store", 
                       type="string", 
                       dest="comment", 
                       help="defines a comment for this migration.", 
                       default ="No Comment")
    parser.add_option( "-j", "--job",  
                       action="store_true", 
                       dest="job", 
                       help="creates migration job, e.g for backups, restores etc.",
                       default=False)
    parser.add_option( "-t", "--table",  
                       action="store", 
                       type="string", 
                       dest="table", 
                       help="set table for migration_job",
                       default="None")
    
    start = None
    end = None 
    start = datetime.datetime.now()
    print "generating migration...."
    
    (options, args) = parser.parse_args()
    #print options
    #TODO: reorg and optimize the section below. more structure.
    #
    if options.model == "None" and not options.job:
        # no model- or job flag given
        if len(args) == 0:
            parser.error("You must at least specify an migration name by giving -n <name>.")
            return
            # if no option flag (like -m) is given, it is assumed 
            #that the first argument is the model. (representing -m arg1)
        else:
            options.model = args[0]
            
    if options.model.startswith("rel_") and ( options.model.count("_") == 2 ):
        # if the name is of the form: rel_name1_name2 it is assumed that you want to
        # generate a relation between name1 and name2. So the mig is especially customized for that.
        print "assuming you want to create a relation migration..."
        
        render_relation_migration(options.model, parts_dir)
        end = datetime.datetime.now()
        duration = None
        duration = end - start 

        print "generated_migration in("+ str(duration) +")"
        return        
            
    else:
        # we got a model or job.
        if options.job:
            render_migration_job(options.job, options.table)
        else: 
            print "    --- for model: %s" % (options.model)
            render_migration(options.model, options.comment)
    
    end = datetime.datetime.now()
    duration = None
    duration = end - start 
    
    print "generated_migration in("+ str(duration) +")"
    print
    return

def render_relation_migration(name, parts_dir=PARTS_DIR , prefix_dir = "./"):
    """
    renders a migration for a relational link between tables / models
    Typical examples are A.has_many(B) and B.belongs_to(A)
    these are then added to the newly genrated migration file.
    
    :params name    =>  name of the migration. Must be of the form rel_modelA_modelB.
                        modelA and modelB are singular forms (like post NOT posts)
    :param PARTS_DIR:   A relative path to the stubs/partials dir from the executing script.
    :param prefix_dir:  A prefix path to be added to migrations making prefix_dir/migrations the target dir
    """

    splittxt = string.split(name, "_")
    model1 = splittxt[1]
    model2 = splittxt[2]
    
    print " -- generate_migration: relation migration for models: " + model1 +  " & " + model2
    print " -- following the naming convention rel_model1_model2"
    print " -- you gave:", name
    
    # add the auto generated (but can be safely edited) warning to the outputfile
    
    infile = open (os.path.normpath(parts_dir + "relation_migration.py"), "r")
    ostr = infile.read()
    infile.close()
    
    # add a creation date
    d = datetime.datetime.now()
    ostr = ostr.replace( "#DATE", d.strftime("%Y/%m/%d %H:%M:%S"))
    # add model1 import
    ostr = ostr.replace( "#UPMODEL1", str.capitalize(model1))
    # add model2 import
    ostr = ostr.replace( "#UPMODEL2", str.capitalize(model2))
    
    # add the example migration for this models
    ostr = ostr.replace( "#MODEL1", model1)
    ostr = ostr.replace( "#MODEL2", model2)
    
    filename = write_migration( name, 
                                "relation between %s and %s" % (model1, model2),
                                prefix_dir,
                                ostr
                                )
    print  " -- created file:" + str(os.path.normpath(os.path.join(prefix_dir,filename)))
    return
    

def write_migration(name, comment, prefix_dir="./", ostr=""):
    """
    Writes a new migration.
    It generates a new version, constructs the correct filename and path
    Updates the App and Version tables and writes ostr to the new filen.
    :param name:    Name of the new migration. 
    :param ostr:    Content that will be written to the new migration.
    """
    version = ObjectId()
    # you can see the time part with: version.generation_time
    print "version: %s  : gen_time: %s " % (version, version.generation_time.strftime("%Y/%m/%d %H:%M:%S"))
    
    # will be saved in the versions table and used to load the module by do_migrate
    filename = str(version) + "_" + name + ".py"
    
    #update the app table with the new version
    update_app_and_version(filename, version, comment )
    
    ofile = open(  os.path.normpath(os.path.join(prefix_dir + "/migrations/", filename)) , "w") 
    ofile.write(ostr)
    ofile.close()
    print "written %s " % (filename)
    return filename
    

    
def update_app_and_version(filename, version, comment=""):
    """
    update the app table with the new version
    update the version table with:
        filename, version and comment (if any).
    """
    pass
    return 
    
def render_migration( modelname="NO_MODEL_GIVEN", comment="", col_defs = "None", 
                      parts_dir=PARTS_DIR, prefix_dir = "./"):
    """
    Renders a database migration file.
    :param model:       Modelname for this migration (typically defining the model's base table)
    :param comment:     a Comment for this migration
    :param col_defs:    pre defined column definitions of the form NAME TYPE OPTIONS, NAME1 TYPE1 OPTIONS1, ...
    :param parts_dir:   A relative path to the stubs/partials dir from the executing script.
    :param prefix_dir:  A prefix path to be added to migrations making prefix_dir/migrations the target dir
    """
    
    # add the auto generated (but can be safely edited) warning to the outputfile
    print os.path.normpath(parts_dir + "migration.py")
    infile = open (os.path.normpath(parts_dir + "migration.py"), "r")
    ostr = infile.read()
    infile.close()

    # Replace the TAGGED Placeholders with the actual values
    d = datetime.datetime.now()
    ostr = ostr.replace( "#DATE", d.strftime("%Y/%m/%d %H:%M:%S"))
    # add model1 import
    ostr = ostr.replace( "#UP_MODELNAME", str.capitalize(modelname))
    
    # replace the Modelname
    ostr = ostr.replace( "#MODELNAME", modelname)
    
    #
    # Add / Replace the column definitions with the given ones by -d (if there were any)
    # 
    if col_defs != "None":
        ostr = transform_col_defs( ostr, col_defs )

    # generate the new version
    #version = get_new_version()
    #verstring = powlib.version_to_string(version)

    print "generate_migration for model: " + modelname

    # really write the migration now
    write_migration(modelname, comment, prefix_dir, ostr)

    return


def render_migration_job(filename, tablename):
        """create a 'job' or task that has to be done on the database.
        typical examples are backup/restore scripts for dbs or tables or loading data into a table.
        These migrations are not part of the migration versioning system.
        They can be executed with python migrate.py -f <migrationname>
        You can set the table by adding the -t <tablename> option
        """
        print " -- creating migration job:"
        infile = open(os.path.normpath( PARTS_DIR + "migration_job.part"), "r")
        instr = infile.read()
        infile.close()
        instr = instr.replace("#JOBNAME", filename+ "_migration.py")
        if tablename != "None":
            instr = instr.replace("#TABLENAME", tablename)
        ofile = open(os.path.normpath( "./migrations/" + filename + "_migration.py"), "w")
        ofile.write(instr)
        ofile.close()
        #powlib.check_copy_file(os.path.normpath( PARTS_DIR + "migration_job.part"), "./migrations/" + filename + "_migration.py")
        return
        

if __name__ == '__main__':
    main()
