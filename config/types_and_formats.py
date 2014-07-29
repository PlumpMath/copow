import #APPNAME.config.uimodules as uimodules
import datetime
from bson.objectid import ObjectId
from #APPNAME.lib.custom_encoders import *
import #APPNAME.uimodules.copow_ui_modules
import #APPNAME.config.uimodules as uimodules

# schema_types dictionary holds the possible document schema types and there copow defaults.
# defaults can be adjusted by giving a default attribuet in the schema.
# Format type : ( default_value, form_uimodule, { custom_encoder, custom_decoder} )
schema_types = {
    "string"    :   (   "", 
                        uimodules.modules["form_textinput"], 
                        {}),
    "text"      :   (   "", 
                        uimodules.modules["form_textarea"],
                        {}),
    "integer"       :   (   0, 
                        uimodules.modules["form_textinput"], 
                        {}),
    "float"     :   (   0.0, 
                        uimodules.modules["form_textinput"], 
                        {}),
    "list"      :   (   [], 
                        uimodules.modules["form_select"], 
                        {   "encode_python"     :   #APPNAME.lib.custom_encoders.list_encode_python,
                            "encode_json"       :   #APPNAME.lib.custom_encoders.list_encode_json,
                            "encode_db"         :   #APPNAME.lib.custom_encoders.list_encode_db,
                            "encode_str"        :   #APPNAME.lib.custom_encoders.list_encode_str
                        }
                    ),
    "binary"    :   (   None, 
                        uimodules.modules["form_fileselect"], 
                        {}),
    "object"    :   (   None, 
                        uimodules.modules["form_textinput"], 
                        {}),
    "date"      :   (   datetime.datetime.now(), 
                        uimodules.modules["form_datepicker"], 
                        {}),
    "objectid"  :   (   ObjectId(), 
                        uimodules.modules["form_textinput"], 
                        {   "encode_python"     :   #APPNAME.lib.custom_encoders.oid_encode_python,
                            "encode_json"       :   #APPNAME.lib.custom_encoders.oid_encode_json,
                            "encode_db"         :   #APPNAME.lib.custom_encoders.oid_encode_db
                        }
                    ),
    "dict"      :   (   {}, 
                        uimodules.modules["form_textarea"], 
                        {}),
    "boolean"      :   (   False, 
                        uimodules.modules["form_checkbox"], 
                        {}),
    "set"       :   (   set(), 
                        uimodules.modules["form_textinput"], 
                        {   "encode_python"     :   #APPNAME.lib.custom_encoders.set_encode_python,
                            "encode_json"       :   #APPNAME.lib.custom_encoders.set_encode_json,
                            "encode_db"         :   #APPNAME.lib.custom_encoders.set_encode_db,
                            "encode_str"        :   #APPNAME.lib.custom_encoders.set_encode_str
                        }
                    )   
}



data_formats = {
    
    # supported result_formats of your Application.
    # By default copow will invoke the method which fits
    # the REST request and end in the tuple[1] name
    # exmaple: Accept: "application/json"   + GET /controller  => controller.list_json()
    # Only applies to methods that return values (show, list) ;)
    # Order of the Accepted incoming HTTP-Header counts (1st come 1st served)

    "accept_formats"        :   {   
                                "text/html"         :       "_html",
                                "application/json"  :       "_json"
                            },

    "content_type_formats"  :  {   
                                "application/x-www-form-urlencoded"         :       "_html",
                                "application/json"                          :       "_json",
                                "multipart/form-data"                       :       "_multipart"
                            },
    "default_function"      :   "_json",
    "default_format"         :   "application/json"
    #"accept_format_dependend_methods"   :   ["list", "show"],
    #"content_type_dependend_methods"    :   ["update"]

}