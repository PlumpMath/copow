#
# Example Hello Controller
# 
import tornado.web
import os
import #APPNAME.config.settings as settings


class BaseController(tornado.web.RequestHandler):
    """ copow base controller 
        Does the neccessary routing for the standard REST requests.
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
        HTTP GET        => will call controller.show(something)
        HTTP POST       => will call Nothing. [returns HTTP 501]
        HTTP PUT        => will call controller.edit(something)
        HTTP DELETE     => will call controller.delete(something)
        and a call to domain:port/controller/
        HTTP GET        => will call controller.list()
        HTTP POST       => will call controller.create()
        HTTP PUT        => will call controller.replace_all() [returns HTTP 501 by default]
        HTTP DELETE     => will call controller.delete_all()

        ***********
        * FORMAT:
        ***********
        Also all reuests can have an Accept: HTTP header field which must be parsed by the
        controller itself.
        Example:    Accept:      text/json
    """
    
    def __init__(self, *args, **kwargs):
        super(BaseController,self).__init__(*args,**kwargs)

    
    def get(self, *args, **kwargs):
       """
            Routing is done RESTful but accoring to the specification ikn routes.py
             r"/#controller/([0-9a-zA-Z]+)"                 :     ("#controller_cls", dict(method="show", params=["id"]))

             Will result in:
             Accept Header = format
             GET /controller-name/id            =>      calls controller.show_format(args, kwargs)
                controller.show_format should eat the params parameter e.g. like this
                def show_json(self, id, *args, **kwargs):
                where format is defined in settings.py
        """
        print("get *args: ", args)
        print("get kwargs: ", kwargs)
        print("self.method: ", self.method)
        print("self.params: ", self.params)
        # Which Output formats do we support ?
        supported_result_formats = settings.base["result_formats"]
        # Which Output formats does the client accept ?
        accepted_result_formats = self.request.headers.get("Accept").split(",")
        
        # try to match them. order matters. 1st come, 1st servec
        for format in accepted_result_formats:
            if format in supported_result_formats.keys():
                # call the defined function (suffix)

                print("requested result formats: ", accepted_result_formats)
                print("returning: ", format)
                return getattr(self,self.method + supported_result_formats[format])(*args, **kwargs)
                # if self.params != []:
                #     print("id: ", id)
                #     if self.method == "update":
                #         return self.update_form(id=id)
                #     else:
                #         #return self.show(id)   
                #         return getattr(self,"show"+supported_result_formats[format])(id=id)
                # else:
                #     #return self.list()
                #     return getattr(self,"list"+supported_result_formats[format])()
                break
        #raise tornado.web.HTTPError(406)
        self.send_error(status_code=406, **kwargs)
        

    def post(self, *args, **kwargs):
        """ 
            Meaning a call to domain:port/controller/([someting]+)
            HTTP POST       => will call Nothing, yet.
            and a call to domain:port/controller/
            HTTP POST       => will call controller.create()
        """
        if args:
            # POST /controller/id   => [returns HTTP 501]
            self.set_status(501)
            self.render("error.html")
        else:
            # POST /controller/     => its create
            id = args[0]
            return self.create(id)

    def put():
        """
            Meaning a call to domain:port/controller/([someting]+)
            HTTP PUT        => will call controller.edit(something)
            and a call to domain:port/controller/
            HTTP PUT        => will call controller.replace_all() [returns HTTP 501]
        """
        if args:
            # PUT /controller/id   => its update(id)
            id = args[0]
            return self.update(id)
        else:
            # PUT /controller/   => it is update_all()
            return self.update_all()
            
    def delete():
        """
            Meaning a call to domain:port/controller/([someting]+)
            HTTP DELETE     => will call controller.delete(something)
            and a call to domain:port/controller/
            HTTP DELETE     => will call controller.delete_all()
        """
        if args:
            # DELETE /controller/id   => its delete(id)
            id = args[0]
            return self.delete(id)
        else:
            # DELETE /controller/   => it is delete_all()
            return self.delete_all()

    ## error handler taken from: https://github.com/CarlosGabaldon/tornado_alley/blob/master/chasing_tornado.py
    def write_error(self, status_code, **kwargs):
        import traceback
        if self.settings.get("debug") and "exc_info" in kwargs:
            exc_info = kwargs["exc_info"]
            trace_info = ''.join(["%s<br/>" % line for line in traceback.format_exception(*exc_info)])
            request_info = ''.join(["<strong>%s</strong>: %s<br/>" % (k, self.request.__dict__[k] ) for k in self.request.__dict__.keys()])
            error = exc_info[1]
            
            self.set_header('Content-Type', 'text/html')
            self.finish("""<html>
                             <title>%s</title>
                             <body>
                                <h2>Error</h2>
                                <p>%s</p>
                                <h2>Traceback</h2>
                                <p>%s</p>
                                <h2>Request Info</h2>
                                <p>%s</p>
                             </body>
                           </html>""" % (error, error, 
                                        trace_info, request_info))

    def get_current_user(self):
        return None

    def get_current_user_role(self):
        return None







