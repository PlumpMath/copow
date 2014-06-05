import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import os.path
import sys

import #APPNAME.config.routes 
import #APPNAME.config.settings

#sys.path.append(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../config" )) 

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

copow_handlers = #APPNAME.config.routes.handlers
copow_settings = #APPNAME.config.settings.webserver

if __name__ == "__main__":
	print (os.path.join(os.path.dirname(__file__)))
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=copow_handlers, settings=copow_settings)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

		