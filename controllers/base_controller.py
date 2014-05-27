#
# Example Hello Controller
# 
import tornado.web
import os

class BaseController(tornado.web.RequestHandler):
    """ copow base controller """
    

    def get_current_user(self):
        return None

    def get_current_user_role(self):
        return None







