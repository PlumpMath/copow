#
# copow REST Dispatch controller
# 
import tornado.web
import os
from #APPNAME.controllers.base_controller import BaseController

class DispatchController(BaseController):
    """ Does the neccessary routing for the standard REST requests.
        Automatically calls the right cotroller->CRUDMethod.
        According to this mapping table:
        **********
        * ACTION:
        **********
        in General:
        HTTP    Method      CRUD Action Description
        -----------------------------------------------
        POST    CREATE      Create a new resource
        GET     RETRIEVE    Retrieve a representation of a resource
        PUT     UPDATE      Update a resource
        DELETE  DELETE      Delete a resource

        PUT and DELETE must be handled with a POST request and an
        addiotional HTTP Parameter: REQUEST_TYPE
        set to PUT or DELETE accordingly.

        Meaning a call to domain:port/controller/([someting]+)
        Where something is usually an ID
        HTTP get        => will call controller.show(something)
        HTTP POST       => will call controller.create(something)
        HTTP PUT        => will call controller.edit(something)
        HTTP DELETE     => will call controller.delete(something)
        and a call to domain:port/controller/
        HTTP get        => will call controller.list()
        HTTP POST       => will call Nothing, yet.
        HTTP PUT        => will call controller.replace_all() [empty by default]
        HTTP DELETE     => will call controller.delete_all()

        ***********
        * FORMAT:
        ***********
        Also all reuests can have an Accept: HTTP header field which must be parsed by the
        controller itself.
        Example:    Accept:      text/json

    """
    def get(self):
        """ nothing """
        

    def post(self):
        """ nothing """