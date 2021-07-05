from datetime import datetime
import json

import cherrypy


class Index:

    def __init__(self):
        pass

    @cherrypy.expose
    @cherrypy.tools.template
    def index(self):
        pass


    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def executequery(self):

        input_json = cherrypy.request.json
        database = input_json["database"]
        query = input_json["query"]
        pass

    @cherrypy.expose
    @cherrypy.tools.template
    def login(self):
        pass
    
    @cherrypy.expose
    def broken(self):
        raise RuntimeError('Pretend something has broken')

def errorPage(status, message, **kwargs):
    return cherrypy.tools.template._engine.get_template('page/error.html').render()