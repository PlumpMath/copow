#!/usr/bin/env python 
## Thx to:
##  http://code.activestate.com/recipes/355319/ (r1)
## eased my life. Console and the  recipe above ;)
import code
import sys,os, string, pdb
from bson.objectid import ObjectId

APPNAME = "#APPNAME"

try:
    import pyreadline as readline
except ImportError:
    try:
        import readline
    except ImportError:
        print("""pow_console needs readline or pyreadline. 
                Please install readline(linux) or pyreadline(wivdows) via""")
        print("pip install (py)readline.")


class FileCacher:
    "Cache the stdout text so we can analyze it before returning it"
    def __init__(self): self.reset()
    def reset(self): self.out = []
    def write(self,line): self.out.append(line)
    def flush(self):
        #output = '\n'.join(self.out)
        output = ''.join(self.out)
        self.reset()
        return output

class Shell(code.InteractiveConsole):
    "Wrapper around Python that can filter input/output to the shell"
    def __init__(self):
        self.stdout = sys.stdout
        self.cache = FileCacher()
        code.InteractiveConsole.__init__(self)
        self.start_save = False
        self.log_file = None
        # importing the pow modules as well as 
        # current Models, Controllers for this project
        importdirs = ["./models/basemodels", "./models", "./controllers" ]
        include_ext_list = [".py"]
        for adir in importdirs:
            sys.path.append(os.path.abspath(adir))
            
        for path in importdirs:
            importlist = []
            for elem in os.listdir(os.path.normpath(path)):
                fname, fext = os.path.splitext(elem)
                if fext in include_ext_list and not fname.startswith("__"):
                    statement = "from "+ str(fname)+ " import *" 
                    print("executing statement: ", statement)
                    #exec statement
                    self.push(statement)
        return
    
    def get_output(self): 
        sys.stdout = self.cache
    
    def return_output(self): 
        sys.stdout = self.stdout

    def push(self,line):
        self.get_output()
        # you can filter input here by doing something like
        #print "hey, this is the input: ", line
        # line = filter(line)
        command = False
        if line == "help":
            print("start_save | end_save => save the console session to console_out.txt")
            print("You can use the standard python console help anyway.")
            command = True
        elif line == "start_save":
            self.start_save = True
            self.log_file = open("console_out.txt", "w")
            #self.log_file.write(os.linesep)
            command = True
        elif line == "end_save":
            command = True
            if self.start_save:
                self.log_file.write("end_save" + os.linesep)
                self.log_file.close()
                self.start_save = False
            else:
                print("error: you can only end_save if you started it first ;)")
        
        if self.start_save and self.log_file:
            #self.log_file.write("Input:" + 2*os.linesep)
            self.log_file.write( line + os.linesep)
        newline = line
        if not command:
            code.InteractiveConsole.push(self,newline)
        self.return_output()
        output = self.cache.flush()
        # you can filter the output here by doing something like
        # output = filter(output)
        if output != "":
            if self.start_save:
                #self.log_file.write("Output for: " + line + 2*os.linesep)
                self.log_file.write( output +  os.linesep)
            print(output) # or do something else with it
        return 

if __name__ == '__main__':
    sh = Shell()
    
    pow_banner = "pow console v0.1 " + os.linesep
    pow_banner += "Using python " + str(sys.version)[:6] + os.linesep
    pow_banner += "type help to get more info and help on special pow_console commands"
     
    sh.interact(pow_banner)
## end of http://code.activestate.com/recipes/355319/ }}}
