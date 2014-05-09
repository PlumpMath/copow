#
# Example Hello Controller
# 
import tornado.web
import os

class HelloController(tornado.web.RequestHandler):
    """docstring """
    def get(self):
        greeting = self.get_argument("greeting", "Hello")
        self.write(greeting + ", friendly user!")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "public")
    }
