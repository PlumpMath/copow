from werkzeug.wrappers import Request, Response
import #APPNAME.config.config as config
import #APPNAME.lib.db_conn as db_conn

APPNAME = "#APPNAME"

#@Request.application
def application(environ, start_response):
    request = Request(environ)
    #text = 'Hello %s!' % request.args.get('name', 'World')
    text = "Hello World"
    db = db_conn.DBConn()
    text += str(db.get_client())
    response = Response(text, mimetype='text/plain')
    return response(environ, start_response)

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    import logging
    
    run_simple(config.base["server"], config.base["port"], application)
