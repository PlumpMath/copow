#
#
# powlib
#
import os
import re
import logging
import datetime
#from .db_conn import DBConn
import string
import shutil
from bson.objectid import ObjectId
import imp

newline = os.linesep
tab = "    "
_logger = None

# schema_types dictionary holds the possible document schema types and there copow defaults.
# defaults can be adjusted by giving a default attribuet in the schema.
# Format type : default
schema_types = {
    "string"    :   "",
    "text"      :   "",
    "int"       :   0,
    "float"     :   0.0,
    "list"      :   [],
    "binary"    :   None,
    "object"    :   None,
    "date"      :   None,
    #"id"        :   ObjectId()
    "id"        :   None
}

#
# (pattern, search, replace) regex english plural rules tuple
# taken from : http://www.daniweb.com/software-development/python/threads/70647
rule_tuple = (
    ('[ml]ouse$', '([ml])ouse$', '\\1ice'),
    ('child$', 'child$', 'children'),
    ('booth$', 'booth$', 'booths'),
    ('foot$', 'foot$', 'feet'),
    ('ooth$', 'ooth$', 'eeth'),
    ('l[eo]af$', 'l([eo])af$', 'l\\1aves'),
    ('sis$', 'sis$', 'ses'),
    ('man$', 'man$', 'men'),
    ('ife$', 'ife$', 'ives'),
    ('eau$', 'eau$', 'eaux'),
    ('lf$', 'lf$', 'lves'),
    ('[sxz]$', '$', 'es'),
    ('[^aeioudgkprt]h$', '$', 'es'),
    ('(qu|[^aeiou])y$', 'y$', 'ies'),
    ('$', '$', 's')
    )

def regex_rules(rules=rule_tuple):
    # also to pluralize
    for line in rules:
        pattern, search, replace = line
        yield lambda word: re.search(pattern, word) and re.sub(search, replace, word)


def get_time_from_objectid(oid, FORMAT_STRING="%Y/%m/%d %H:%M:%S"):
    return oid.generation_time.strftime(FORMAT_STRING)

def get_time():
    return get_time_from_objectid(ObjectId())


def plural(noun):
    #print noun
    # the final pluralisation method.
    for rule in regex_rules():
        result = rule(noun)
        #print result
        if result:
            return result

def pluralize(noun):
    return plural(noun)

def singularize(word):
    # taken from:http://codelog.blogial.com/2008/07/27/singular-form-of-a-word-in-python/
    sing_rules = [lambda w: w[-3:] == 'ies' and w[:-3] + 'y',
              lambda w: w[-4:] == 'ives' and w[:-4] + 'ife',
              lambda w: w[-3:] == 'ves' and w[:-3] + 'f',
              lambda w: w[-2:] == 'es' and w[:-2],
              lambda w: w[-1:] == 's' and w[:-1],
              lambda w: w,
              ]
    word = word.strip()
    singleword = [f(word) for f in sing_rules if f(word) is not False][0]
    return singleword

def p2c(name):
    """ (alias for:) pluralname to classname. So posts becomes Post"""
    return plural_to_classname(name)

def plural_to_classname(name):
    """ pluralname to classname. So posts becomes Post"""
    return string.capitalize(singularize(name))

def load_class(path_to_module, cls):
    """
        param: path_to_module = path to the module without the Appname
               so to load a model user just give: models.user
        param: cls = classname to load
        returns: the imported class

    """
    module = __import__("#APPNAME" + "." + path_to_module, globals(), locals(), [cls], 0)        
    module= imp.reload(module)
    ret = module.__dict__[cls]
    acls = ret()
    return acls

def logtime_now():
    return 

def _log(type, message):
    pass

# loger from werkzeug
def _log_stream(type, message, *args, **kwargs):
    """Log into the internal werkzeug logger."""
    global _logger 
    if _logger is None:
        import logging
        _logger = logging.getLogger('pow')
        # Only set up a default log handler if the
        # end-user application didn't set anything up.
        if not logging.root.handlers and _logger.level == logging.NOTSET:
            _logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            _logger.addHandler(handler)
    getattr(_logger, type)(message.rstrip(), *args, **kwargs)


# coroutine.py
#
# A decorator function that takes care of starting a coroutine
# automatically on call. (by calling next automatically for us)
# taken from the brilliant site of dabaez: check: http://www.dabeaz.com/coroutines/coroutine.py
# 
def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        next(cr)
        return cr
    return start
# Example use
#if __name__ == '__main__':
#    @coroutine
#    def grep(pattern):
#        print "Looking for %s" % pattern
#        while True:
#            line = (yield)
#            if pattern in line:
#                print line,

def check_create_dir( path ):
    ret = False
    #print "checking for " + path +"...\t" ,
    if os.path.isdir( os.path.normpath(path) ):
        print(" exists" +"...\t",)
        ret=False
    else:
        os.mkdir( os.path.normpath(path) )
        print(" created" +"...\t",)
        ret=True
    print(os.path.normpath(path))
    return ret


def check_create_file( path, filename ):
    ret = False
    #print "checking for " + os.path.normpath(os.path.join(path, filename)) + "...\t" ,
    if os.path.isfile( os.path.normpath(os.path.join(path, filename))):
        print(" exists" +"...\t")
        ret = False
    else:
        file = open(os.path.normpath(os.path.join(path, filename)),"w")
        file.close()
        print(" created" +"...\t")
        ret = True
    print(os.path.normpath(os.path.join(path, filename)))
    return ret


def check_copy_file( src, dest, new_name=None, force=True, replace=None):
    """
        checks if file exists and copies if not (force overwrites that)
        src = src file including path
        dest = dest DIR only
        force = force overwrite existing file
        if replace_list != [] this function also replaces strings in the files
        replace = [(string_to_find, string_replacement),....]
    """
    ret = False
    src_path, src_file = os.path.split(src)
    if new_name:
        dest_file = new_name
    else:
        dest_file = src_file
    dest_path = dest
    #print("src: ", src)
    dest_abs = os.path.abspath(os.path.normpath(os.path.join(dest_path, dest_file)))
    #print("dest_abs: ", dest_abs)
    if os.path.isfile(dest_abs) and force == False:
        #src_path, src_file = os.path.split(src)
        print(" exists and skipping (force==False) ...\t", dest_abs)
        return False
    else:
        if not os.path.isdir( os.path.normpath(src) ):
            try:
                shutil.copy(src,dest_abs)
                #if dest:
                #    print ("src: ", src)
                #    print("dest:", dest)
                if replace:
                    #dest = os.path.normpath(os.path.abspath(os.path.join(dest, src)))
                    replace_string_in_file(dest_abs,replace)
                print(" copied" + "...\t", src)
                return True
            except IOError as xxx_todo_changeme:
                (errno, strerror) = xxx_todo_changeme.args
                print(" I/O error...(%s): %s. File: %s" % (errno, strerror, src, dest_abs))
                return False
        else:
            print(" skipped...DIR\t", src)

    return True

def replace_string_in_file( absfilename, replace_list=[] ):
    """
        replaces the given sting in a file
        absfilename = absolute_path_to_src_file
        replace_list = [(string_to_find, string_replacement),....]
    """
    # set correct Appname in pow_router.wsgi
    #print("replacing in:", absfilename)
    f = open(absfilename, "r")
    instr = f.read()
    for tupel in replace_list:
        origstr = tupel[0]
        repstr = tupel[1]
        instr = instr.replace(origstr, repstr)
    f.close()
    f = open(absfilename, "w")
    f.write(instr)
    f.close()
    return