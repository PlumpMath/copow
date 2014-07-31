#
# Example Hello Controller
# 
import tornado.web
import os
from #APPNAME.controllers.base_controller import BaseController

class WelcomeController(BaseController):
    """docstring """
    def prepare(self):
        """ called before any http get/pust method is called """
        pass


    def get(self):
        uri = self.request.uri
        if uri =="/welcome":
            self.render("welcome.html", argslist=self.path_args, kwargslist=self.path_kwargs, request=self.request)
        elif uri == "/features":
            self.render("features.html")
        elif uri == "/twitter":
            self.render("twitter.html")
        elif uri == "/next-steps":
            self.render("next-steps.html")
        else:
            self.render("welcome.html", argslist=self.path_args, kwargslist=self.path_kwargs, request=self.request, loginname=None)






