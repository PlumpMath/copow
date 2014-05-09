
#
# All the copow 'global' configutration goes here
#
base = {
	
	"server"		:	"localhost",
	"port"			:	8080,
	"environment"	:	"development",
	# Standard Directories
	"parts_dir"		:	"stubs/templates/",
	"model_test_dir" :	"test/models/",
}

logging=  {
	
	"clear_log_at_startup"	: True,
	"format"				: "#DATE,#TIME,#LEVEL,#MESSAGE"
}

# for the webserver_settings
# See: http://www.tornadoweb.org/en/stable/web.html 
# section: Application configuration
# 

webserver = {
    #  Setting debug=True is equivalent to autoreload=True, compiled_template_cache=False, 
    #                     static_hash_cache=False, serve_traceback=True.
    "debug"     :   True
    #default_handler_class and default_handler_args: This handler will be used if no other 
    # match is found; use this to implement custom 404 pages (new in Tornado 3.2).

    # cookie_secret: Used by RequestHandler.get_secure_cookie and set_secure_cookie to sign cookies.
    
    # login_url: The authenticated decorator will redirect to this url if the 
    #   user is not logged in. Can be further customized by overriding RequestHandler.get_login_url
    
}