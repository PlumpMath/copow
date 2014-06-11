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
import shutil
from #APPNAME.models import app
from #APPNAME.models import version

import #APPNAME.lib.powlib as powlib
import #APPNAME.config.settings as settings 


def main():
    parser = OptionParser()

    parser.add_option("-m", "--model",
                      action="store",
                      type="string",
                      dest="model",
                      help="model to create the scaffolding for",
                      default="None")
    parser.add_option("-f", "--force",  
                      action="store_true",  
                      dest="force", 
                      help="forces overrides of existing files",
                      default=False)

    (options, args) = parser.parse_args()
    #print options
    

    start = None
    end = None
    start = datetime.datetime.now()

    if options.model == "None":
        if len(args) > 0:
            # if no option flag (like -m) is given, it is assumed that
            # the first argument is the model. (representing -m arg1)
            options.model = args[0]
        else:
            parser.error(
                "You must at least specify a model by giving -m <model>."
            )

    generate_scaffold(options.model, force=options.force)


    end = datetime.datetime.now()
    duration = None
    duration = end - start
    print(" generated scaffolds in (" + str(duration) + ")")


def generate_scaffold( modelname, force=False ):
    """
        Generate the vies scaffolding for a given model. 
        Templates can be found in stubs/templates. 

    """
    #views = ["create", "create_form","list", "show", "update", "update_form", "update_all", "delete" ]
    
    views = ["list", "show", "echo"]
    
    for view in views:
        template_in_path = os.path.join(os.path.normpath(settings.base["parts_dir"]), view + ".html")
        view_out_path = os.path.join("./", "views")
        current_path = __file__
        print("template in: ", template_in_path)
        print("view out: ", view_out_path)
        print("  -- generating scaffold for: ", modelname + "_" + view)
        powlib.check_copy_file( template_in_path, view_out_path,  
                    new_name = modelname +  "_" + view + ".html",
                    force = force )


if __name__ == '__main__':
    main()
