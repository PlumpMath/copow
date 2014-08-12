#
# Example Hello Controller
# 
import tornado.web
import os
import json
import #APPNAME.config.settings as settings
import #APPNAME.config.types_and_formats as types_and_formats
import #APPNAME.ext.user_management as umgmt
import #APPNAME.models.user as user

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
        self.current_user = None
        self.data = None
        super(BaseController,self).__init__(*args,**kwargs)

    def get_request_body_json_data(self, request):
        return json.loads(request.body.decode(settings.base["default_encoding"]))


    def convert_html_to_json(self, request):
        """ converts incoming html-form-data to json 
            it is important that the params returned as json are only
            those which you defoied in config/routes for the according request.

            example: params_post =["login", "password"] 
        """
        params = getattr(self, "params_" + self.request.method.lower())
        d = {}
        for param in params:
            d[param] = self.get_argument(param, None)
        return d

    def get_format_and_charset(self, format):
        # typical example with charset: ["applicatio/json; charset=UTF-8"]
        # typical example without charset: ["text/html"]
        l=format.split(";")
        #if len(l) > 1:
        #    format = l[0]
        #    charset= l[1][l[1].index("=")+1:]
        #else:
        #    format=l[0]
        #    charset="UTF-8"
        format=l[0]
        charset="UTF-8"
        return format,charset

    def get_preferred_format(self, req_formats, supported_formats):
        """ input is a lis of content-type header formats.
            example: ['text/html', 'application/json; charset=utf-8', 'application/xml]
            charsets are currently dropped
        """
        # Which Output formats does the client accept ?
        
        requested_formats_encodings = []
        requested_formats = []
        for f in req_formats:
                # TODO: Implement charset checking here:
                format,charset = self.get_format_and_charset(f)
                requested_formats.append(format)
                requested_formats_encodings.append(charset)      

        print("  -- request formats: ", requested_formats)
        #print("  -- request charsets: ", requested_formats_encodings)
        # try to match them. order matters. 1st come, 1st servec
        
        for format in requested_formats:
            if format in supported_formats.keys():
                # call the defined function (suffix)
                print("  -- returning: ", format)
                return format
                break
        #
        # unsupported format request, returning default:
        #
        return types_and_formats.data_formats["default_format"]

    def initialize(self,    method_get=None, params_get = None, 
                            method_put=None, params_put = None,
                            method_post=None, params_post = None,
                            method_delete=None, params_delete = None
                            ):
        """
            The paramter method is set to the value defined in the dict
            in routes->rest_routes.
            You can define your own parameters there.
            This is specifically used to route the request (call the following method in the controller)
            which is specified as the 3rd parameter in rest_routes.
            
        """
        self.method_get = method_get
        self.method_put = method_put
        self.method_post = method_post
        self.method_delete = method_delete
        self.params_get = params_get
        self.params_put = params_put
        self.params_post = params_post
        self.params_delete = params_delete
        #print("self.method: ", self.method, "  ->  ", self.params)

    def set_parameters(self, args, params):
        """ gets a list of parameters apllied to this call (in routes)
            and gets the accorgin value from the args tupel
            fills the self.parameters dictionary with the according key, value pairs.
        """
        num = 0
        for elem in params:
            print("setting parameter: ", elem)
            self.parameters[elem] = args[num]
            num += 1

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
        print("self.params: ", self.params_get)
        # Which Output formats do we support ?
        supported_formats = types_and_formats.data_formats["accept_formats"]
        # Which Output formats does the client accept ?
        requested_formats = self.request.headers.get("Accept").split(",")
        
        format = self.get_preferred_format(requested_formats, supported_formats)
        if format != types_and_formats.data_formats["default_format"]:
                    # 
                    # convert any non default input formats to the default (which is json)
                    # 
                    self.data = getattr(self, "convert" + 
                                types_and_formats.data_formats["accept_formats"][format] + "_to" + 
                                types_and_formats.data_formats["default_function"])

        self.set_parameters(args, self.params_get)
        return getattr(self,self.method_get + supported_formats[format])(*args, **kwargs)
        
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
        print("self.params: ", self.params_post)
        # Which Output formats do we support ?
        supported_formats = types_and_formats.data_formats["content_type_formats"]
        # Which Output formats does the client accept ?
        requested_formats = self.request.headers.get("Content-Type").split(",")
    
        format = self.get_preferred_format(requested_formats, supported_formats)
        if format != types_and_formats.data_formats["default_format"]:
                    # 
                    # convert any non default input formats to the default (which is json)
                    # 
                    self.data = getattr(self, "convert" + 
                                types_and_formats.data_formats["content_type_formats"][format] + "_to" + 
                                types_and_formats.data_formats["default_function"])
        
        self.set_parameters(args, self.params_get)
        try:
            return getattr(self,self.method_post + supported_formats[format])(*args, **kwargs)
        except:    
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
        print("self.params: ", self.params_put)
        # Which Output formats do we support ?
        supported_formats = types_and_formats.data_formats["content_type_formats"]
        requested_formats = self.request.headers.get("Content-Type").split(",")
        
        format = self.get_preferred_format(requested_formats, supported_formats)
        if format != types_and_formats.data_formats["default_format"]:
                    # 
                    # convert any non default input formats to the default (which is json)
                    # 
                    self.data = getattr(self, "convert" + 
                                types_and_formats.data_formats["content_type_formats"][format] + "_to" + 
                                types_and_formats.data_formats["default_function"])
        
        self.set_parameters(args, self.params_get)
        try:
            return getattr(self,self.method_put + supported_formats[format])(*args, **kwargs)
        except:
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
        supported_formats = types_and_formats.data_formats["content_type_formats"]
        requested_formats = self.request.headers.get("Content-Type").split(",")
        
        format = self.get_preferred_format(requested_formats, supported_formats)
        if format != types_and_formats.data_formats["default_format"]:
                    # 
                    # convert any non default input formats to the default (which is json)
                    # 
                    self.data = getattr(self, "convert" + 
                                types_and_formats.data_formats["content_type_formats"][format] + "to" + 
                                types_and_formats.data_formats["default_function"])
        
        self.set_parameters(args, self.params_get)
        try:
            return getattr(self,self.method_delete + supported_formats[format])(*args, **kwargs)
        except:
            # if non supported format: raise Error 406
            # raise tornado.web.HTTPError(406)
            self.send_error(status_code=406, **kwargs)

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
    def set_current_user(self, loginname, password):
        u = user.User()
        res = u.find_one( { "loginname" : loginname })
        print("set_current_user:", res)
        if res:
            if umgmt.check_password( res, password ):
                self.current_user = res
                if not self.get_secure_cookie("loginname"):
                    self.set_secure_cookie("loginname", loginname)
                return True    
        return False

    def get_current_user(self):
        if self.current_user:
            return self.current_user
        else:
            return False

        

    def get_current_user_role(self):
        return None







