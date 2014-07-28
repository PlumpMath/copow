#
# All the copow 'global' configutration goes here
#
import os
import os.path
from bson.objectid import ObjectId
import datetime
import #APPNAME.config.uimodules as uimodules


base = {
    
    "server"            :   "localhost",
    "port"              :   8000,
    "environment"       :   "development",
    # Standard Directories
    "parts_dir"         :   "stubs/templates/",
    "view_parts_dir"    :   "stubs/views/",
    "model_test_dir"    :   "test/models/",
    #authentication can be user or role (for now)
    "authentication"    :   "user",
    "default_encoding"  :   "utf-8"
}

# for the webserver_settings
# See: http://www.tornadoweb.org/en/stable/web.html 
# section: Application configuration
# 

webserver = {
    #  Setting debug=True is equivalent to autoreload=True, compiled_template_cache=False, 
    #                     static_hash_cache=False, serve_traceback=True.
    "debug"         :   True,    
    "template_path" : os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(__file__), "../views"))),
    "static_path"   : os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(__file__), "../public"))),
    "cookie_secret" : "bZJc2207WbQLKos6GkHn/1104wQt8S0R0kRvJ5/gaga",
    #"xsrf_cookies" : True,
    "login_url"     : "/login",
    #"base_handler_class"    :   "#APPNAME.controllers.welcome_controller.WelcomeController"
    "ui_modules"    :  uimodules.modules
}

logging =  {
    
    "clear_log_at_startup"  : True,
    "format"                : "#DATE,#TIME,#LEVEL,#MESSAGE"
}