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

        The actual implementation for your application is defined
        in config/routes.py. See section rest_routes.
        It will be also printed to the console when you start server.py

        ***********
        * FORMAT:
        ***********
        Also all reuests can have an Accept: HTTP header field which must be parsed by the
        controller itself.
        Example:    Accept:      text/json
    """
    
    def __init__(self, *args, **kwargs):
        super(BaseController,self).__init__(*args,**kwargs)

    def get_format_and_charset(self, format):
        # typical example with charset: ["applicatio/json; charset=UTF-8"]
        # typical example without charset: ["text/html"]
        l=format.split(";")
        if len(l) > 1:
            format = l[0]
            charset= l[1][l[1].index("=")+1:]
        else:
            format=l[0]
            charset="UTF-8"
        return format,charset

    @tornado.web.removeslash
    def get(self, *args, **kwargs):
        """
            Routing is done RESTful but accoring to the specification ikn routes.py
                r"/#controller/([0-9a-zA-Z]+)"  :   ("#controller_cls", dict(method="show", params=["id"]))

             Will result in:
             ----------------
                Accept Header = format
                GET /controller-name/id            =>      calls controller.show_format(args, kwargs)
                
                controller.show_format should eat the params parameter e.g. like this
                def show_json(self, id, *args, **kwargs):
                
                where format is defined in settings.py
        """
        print("get *args: ", args)
        print("get kwargs: ", kwargs)
        print("self.method_get: ", self.method_get)
        print("self.params: ", self.params)
        # Which Output formats do we support ?
        supported_formats = settings.data_formats["accept_formats"]
        # Which Output formats does the client accept ?
        requested_formats = self.request.headers.get("Accept").split(",")
        
        # try to match them. order matters. 1st come, 1st served
        print("  -- requested result formats: ", requested_formats)
        for format in requested_formats:
            # try to find a supporting method to serve the request
            if format in supported_formats.keys():
                # call the defined function (suffix)
                print("  -- returning: ", format)
                return getattr(self,self.method_get + supported_formats[format])(*args, **kwargs)
                break
        # if we are here it means that we cannot serve any of the requested formats.
        # Returning the default format (Standard is: _json)
        return getattr(self,self.method_get + settings.data_formats["default"])(*args, **kwargs)
        #raise tornado.web.HTTPError(406)
        self.send_error(status_code=406, **kwargs)
        
    @tornado.web.removeslash
    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        """ 
            HTTP POST /controller/<id>/ will call the
            method defined in routes.py POST (method_post)
        """
        print("post *args: ", args)
        print("post kwargs: ", kwargs)
        print("self.method_post: ", self.method_post)
        print("self.params: ", self.params)
        # Which Output formats do we support ?
        supported_formats = settings.data_formats["content_type_formats"]
        # Which Output formats does the client accept ?
        requested_formats = self.request.headers.get("Content-Type").split(",")
        requested_formats_encodings = []
        for format in requested_formats:
                # TODO: Implement charset checking here:
                pass
        print("  -- request formats: ", requested_formats)
        # try to match them. order matters. 1st come, 1st servec
        
        for format in requested_formats:
            if format in supported_formats.keys():
                # call the defined function (suffix)
                print("  -- returning: ", format)
                return getattr(self,self.method_post + supported_formats[format])(*args, **kwargs)
                break
        
        # if non supported format: raise Error 406
        # raise tornado.web.HTTPError(406)
        self.send_error(status_code=406, **kwargs)

    @tornado.web.removeslash
    #@tornado.web.asynchronous
    def put(self, *args, **kwargs):
        """
            Meaning a call to domain:port/controller/
            HTTP PUT        => will call controller.create(something)
            and a call to domain:port/controller/
            HTTP PUT        => will call controller.replace_all() [returns HTTP 501]
        """
        print("put *args: ", args)
        print("put kwargs: ", kwargs)
        print("self.method_put: ", self.method_put)
        print("self.params: ", self.params)
        # Which Output formats do we support ?
        supported_formats = settings.data_formats["content_type_formats"]
        # Which Output formats does the client accept ?
        
        req_formats = self.request.headers.get("Content-Type").split(",")
        requested_formats_encodings = []
        requested_formats = []
        for f in req_formats:
                # TODO: Implement charset checking here:
                format,charset = self.get_format_and_charset(f)
                requested_formats.append(format)
                requested_formats_encodings.append(charset)      

        print("  -- request formats: ", requested_formats)
        print("  -- request charsets: ", requested_formats_encodings)
        # try to match them. order matters. 1st come, 1st servec
        
        for format in requested_formats:
            if format in supported_formats.keys():
                # call the defined function (suffix)
                print("  -- returning: ", format)
                return getattr(self,self.method_put + supported_formats[format])(*args, **kwargs)
                break
        
        # if non supported format: raise Error 406
        # raise tornado.web.HTTPError(406)
        self.send_error(status_code=406, **kwargs)
    
    @tornado.web.removeslash
    @tornado.web.asynchronous
    def delete(self, *args, **kwargs):
        """
            Meaning a call to domain:port/controller/([id]+)
            HTTP DELETE     => will call controller.delete(something)
            and a call to domain:port/controller/
            HTTP DELETE     => will call controller.delete_all()
                            => delete_all is not implemented yet.
        """
        print("delete *args: ", args)
        print("delete kwargs: ", kwargs)
        print("self.method_delete: ", self.method_delete)
        print("self.params: ", self.params)
        return self.delete(*args, **kwargs)

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







