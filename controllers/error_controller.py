#
# Error Handling
# 
import tornado.web
import os
from #APPNAME.controllers.base_controller import BaseController

class ErrorController(BaseController):
    """docstring """
    def get(self):
        self.render("error.html")





