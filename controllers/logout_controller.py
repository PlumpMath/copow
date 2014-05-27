#
# copow default LogoutController
# 
import tornado.web
import os

from #APPNAME.controllers.base_controller import BaseController

class LogoutController(BaseController):
    def get(self):
        if (self.get_argument("logout", None)):
            self.clear_cookie("username")
            self.redirect("/")