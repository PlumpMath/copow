
#
# All the copow 'global' configutration goes here
#
import os
import os.path
from bson.objectid import ObjectId
import #APPNAME.uimodules.copow_ui_modules
import #APPNAME.config.uimodules as uimodules
from #APPNAME.lib.custom_encoders import *

base = {
    
    "server"            :   "localhost",
    "port"              :   8000,
    "environment"       :   "development",
    # Standard Directories
    "parts_dir"         :   "stubs/templates/",
    "view_parts_dir"    :   "stubs/views/",
    "model_test_dir"    :  "test/models/",
    #authentication can be user or role (for now)
    "authentication"    :   "user",
    "default_encoding"  :   "utf-8"
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
    "ui_modules"    :  uimodules.modules
}

# schema_types dictionary holds the possible document schema types and there copow defaults.
# defaults can be adjusted by giving a default attribuet in the schema.
# Format type : ( default_value, form_uimodule, { custom_encoder, custom_decoder} )
schema_types = {
    "string"    :   ("", uimodules.modules["form_textinput"], {}),
    "text"      :   ("", uimodules.modules["form_textarea"], {}),
    "int"       :   (0, uimodules.modules["form_textinput"], {}),
    "float"     :   (0.0, uimodules.modules["form_textinput"], {}),
    "list"      :   ([], uimodules.modules["form_select"], {}),
    "binary"    :   (None, uimodules.modules["form_fileselect"], {}),
    "object"    :   (None, uimodules.modules["form_textinput"], {}),
    "date"      :   (None, uimodules.modules["form_datepicker"], {}),
    "objectid"  :   (ObjectId(), uimodules.modules["form_textinput"], 
                            {   "encode"    :   #APPNAME.lib.custom_encoders.encode_oid,
                                "decode"    :   #APPNAME.lib.custom_encoders.decode_oid
                            }
                    ),
    "id"        :   (None, uimodules.modules["form_textinput"], {}),
    "dict"      :   ({}, uimodules.modules["form_textarea"], {}),
    "bool"      :   (False, uimodules.modules["form_checkbox"], {}),
    "set"       :   (set(), uimodules.modules["form_textinput"], 
                            {   "encode"    :   #APPNAME.lib.custom_encoders.encode_set,
                                "decode"    :   #APPNAME.lib.custom_encoders.decode_set
                            }
                    )   
}

data_formats = {
    
    # supported result_formats of your Application.
    # By default copow will invoke the method which fits
    # the REST request and end in the tuple[1] name
    # exmaple: Accept: "application/json"   + GET /controller  => controller.list_json()
    # Only applies to methods that return values (show, list) ;)
    # Order of the Accepted Header counts (1st come 1st served)
    "accept_formats"        :   {   
                                "text/html"         :       "_html",
                                "application/json"  :       "_json"
                            },

    "content_type_formats"  :  {   
                                "application/x-www-form-urlencoded"         :       "_html",
                                "application/json"                          :       "_json",
                                "multipart/form-data"                       :       "_multipart"
                            },
    "default"               :   "_json"
    #"accept_format_dependend_methods"   :   ["list", "show"],
    #"content_type_dependend_methods"    :   ["update"]

}