
#
# All the copow 'global' configutration goes here
#
import os
import os.path

base = {
    
    "server"            :   "localhost",
    "port"              :   8080,
    "environment"       :   "development",
    # Standard Directories
    "parts_dir"         :   "stubs/templates/",
    "model_test_dir"    :  "test/models/",
    #authentication can be user or role (for now)
    "authentication"   :   "user",
    # supported result_formats of your Application.
    # By default copow will invoke the method which fits
    # the REST request and end in the tuple[1] name
    # exmaple: Accept: "application/json"   + GET /controller  => controller.list_json()
    # Only applies to methods that return values (show, list) ;)
    # Order of the Accepted Header counts (1st come 1st served)
    "result_formats"    :   {   "text/html"         :       "_html",
                                "application/json"  :       "_json"
                            }
}

logging=  {
    
    "clear_log_at_startup"  : True,
    "format"                : "#DATE,#TIME,#LEVEL,#MESSAGE"
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
    
}