#
# Example Hello Controller
# 
import tornado.web
import os
from #APPNAME.controllers.base_controller import BaseController

class WelcomeController(BaseController):
    """docstring """
    def get(self):
        self.render("main.html")


