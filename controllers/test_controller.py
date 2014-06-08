#
# Example Test Controller
# 
import tornado.web
import os
from atest.controllers.base_controller import BaseController

class TestController(BaseController):
    """docstring """
    def prepare(self):
        """ called before any http get/pust method is called """
        pass

    def update(self, *args,**kwargs):
    	self.render("test.html", args=args, method="update", request=self.request)

    
        