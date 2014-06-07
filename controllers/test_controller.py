#
# Example Hello Controller
# 
import tornado.web
import os
from atest.controllers.base_controller import BaseController

class TestController(BaseController):
    """docstring """
    def prepare(self):
        """ called before any http get/pust method is called """
        pass


    def get(self, *args, **kwargs):
        if args:
            # it is show
            method = "show"
            which = args[0]
        else:
            # it is list:
            method = "list"
            which = "all"
        self.render("test.html", method=method, which=which)
        