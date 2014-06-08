#
# Example Hello Controller
# 
import tornado.web
import os

class BaseController(tornado.web.RequestHandler):
    """ copow base controller """
    
    def get(self, *args, **kwargs):
        if args:
            # it is show
            method = "show"
            which = args[0]
            return self.show(which)
        else:
            # it is list:
            method = "list"
            which = "all"
            return self.list()
        #self.render("test.html", method=method, which=which)

    def post(self, *args, **kwargs):
        return self.update(*args,**kwargs)

    def put():
        pass

    def delete():
        pass


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







