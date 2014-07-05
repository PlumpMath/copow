#!python
#  pow controller generator.
#
# options are: 
#   see: python generate_controller.py --help

import os
from optparse import OptionParser
import sys
import string
import datetime


import #APPNAME.lib.powlib
from #APPNAME.config import settings as settings
from #APPNAME.models.app import App
from #APPNAME.lib import powlib as powlib

# setting the right defaults

PARTS_DIR = settings.base["parts_dir"]
CONTROLLER_TEST_DIR = "/tests/controllers/"


def main():
    """ 
        Executes the render methods to generate a conroller and basic 
        tests according to the given options
    """
    parser = OptionParser()
    parser.add_option("-n", "--name",  action="store", type="string", 
                        dest="name", 
                        help="creates migration with name = <name>", 
                        default ="None")
    parser.add_option("-m", "--model",  
                        action="store", 
                        type="string", 
                        dest="model", 
                        help="defines the model for this controller.", 
                        default ="None")
    parser.add_option("-f", "--force",  
                        action="store_true",  
                        dest="force", 
                        help="forces overrides of existing files",
                        default=False)
    parser.add_option("-z", "--zero-tornado",  
                        action="store_true",  
                        dest="zero", 
                        help="forces a controller withoujt any tornado inheritance",
                        default=False)
    
    controller_name = "None"
    controller_model = "None"
    start = None
    end = None
    start = datetime.datetime.now()
    
    (options, args) = parser.parse_args()
    #print options        
    if options.model == "None":
        if len(args) > 0:
            # if no option flag (like -m) is given, it is assumed that 
            # the first argument is the model. (representing -m arg1)
            options.model = args[0]
        else:
            parser.error("You must at least specify an controllername by giving -n <name>.")
            
    controller_name = options.model
    parts_dir = settings.base["parts_dir"]
    render_controller(controller_name, options.force, parts_dir, options.zero)

    end = datetime.datetime.now()
    duration = None
    duration = end - start 
    print("generated_controller in("+ str(duration) +")")
    print()
    return
    
def render_controller(  name="NO_NAME_GIVEN", force=False,  parts_dir="", 
                        zero_tornado=False, prefix_path="./"):
    
    """ generates a controller according to the given options
        @param name: name prefix of the Controller fullname NameController
        @param force: if true: forces overwrtiting existing controllers"""
    width=50
    print("-"*width)
    print("generate_controller: ", name )
    print("-"*width)
    # add the auto generated warning to the outputfile
    if zero_tornado:
        infile = open (os.path.normpath( os.path.join(parts_dir +  "zero_tornado_controller.py")), "r")
    else:
        infile = open (os.path.normpath( os.path.join(parts_dir +  "controller.py")), "r")

    ostr = infile.read()
    infile.close()
    
    #pluralname = powlib.plural(model)
    ostr = ostr.replace( "#DATE", str(datetime.date.today()) )  
    
    ostr = ostr.replace("#CONTROLLER_CAPITALIZED_NAME", name.capitalize())
    ostr = ostr.replace("#CONTROLLER_LOWER_NAME", name)
    ostr = ostr.replace("#MODELNAME_PLURAL", powlib.pluralize(name))
    ostr = ostr.replace("#MODELCLASSNAME", name.capitalize())
    ostr = ostr.replace("#MODELNAME", name)
    filename = os.path.normpath ( 
        os.path.join( prefix_path + "./controllers/",  name + "_controller.py" ) )
    
    if os.path.isfile( os.path.normpath(filename) ):
        if not force:
            print(" --", filename,)
            print(" already exists... (Not overwritten. Use -f to force ovewride)")
        else:
            ofile = open(  filename , "w+") 
            print(" -- created controller " + filename)
            ofile.write( ostr )
            ofile.close()
    else:
        ofile = open(  filename , "w+") 
        print(" -- created controller " + filename)
        ofile.write( ostr )
        ofile.close()
    
    #render_test_stub( name, classname )
    return
    
    
def render_test_stub (controllername, classname, prefix_path ="./" ):
    """ renders the basic testcase for a PoW Controller """
    #print "rendering Testcase for:", classname, " ", " ", controllername
    print(" -- generating TestCase...",)
    infile = open( os.path.normpath( PARTS_DIR +  "test_controller_stub.part"), "r")
    instr = infile.read()
    infile.close()
    test_name = "Test" + classname + ".py"
    
    ofile = open( 
        os.path.normpath(
            os.path.join(prefix_path + CONTROLLER_TEST_DIR, test_name ) ), "w")
    
    instr = instr.replace("#CLASSNAME", "Test" + classname  )
    instr = instr.replace( "#DATE", str(datetime.date.today()) )  
    ofile.write(instr)
    
    ofile.close()
    print(" %s...(created)" % (prefix_path + CONTROLLER_TEST_DIR + test_name))
    return


if __name__ == '__main__':
    main()
