
import cherrypy
import os, tempfile, sys, socket, re
import ConfigParser, importlib
from StringIO import StringIO

sys.path.append("./modules")
import util, bconfig

serverHostname = socket.gethostname()
servicePort = 9999
cherrypy.config.update({'server.socket_host':serverHostname, 'server.socket_port': servicePort,})
cherrypy.config.update({'response.timeout': 10*60})

def jsonify_tool_callback(*args, **kwargs):
    response = cherrypy.response
    response.headers['Content-Type'] = 'application/json'
cherrypy.tools.jsonify = cherrypy.Tool('before_finalize', jsonify_tool_callback, priority=30)

class App(object):

    def permission_check(self):
        try:
            cookie = cherrypy.request.headers['Cookie']
            roles = re.search('BY=(.*?)roles%3D(.*?)(%26|;)', cookie).group(2)
            userid = re.search('BY=(.*?)userid%3D(.*?)%26', cookie).group(2)
            # app_id 11353 maintains the authenticated user whitelist
            # https://by.bouncer.login.yahoo.com/admin/index.html?act=viewappusers&app_id=11353
            return ('%7C11353.' in roles, userid)
        except:
            return (True, 'unknown')

    @cherrypy.expose
    def index(self, **args):
        access, userid = self.permission_check()
        if not access:
            return file('./templates/help.html')
        else:
            content = "".join(file('./templates/index.html').readlines())
            ret = self.prepare(args.get('page'), content)
            return StringIO(unicode(ret))

    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def query(self, **args):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        access, userid = self.permission_check()
        if not access:
            return {'error': "".join(file('./templates/help.html').readlines())}
        else:
            return self.process(args)
    
    def process(self, args):
        action = args.get('action')
        
        try:
            executor = importlib.import_module(action)
        except Exception as e:
            print '[WARN] no %s module found, use default brick' % (action)
            print e
            executor = importlib.import_module('brick')

        print executor
        result = executor.execute(self.config, action, args)
        
        ret = util.json_to_str(result)
        print ret[:1000]
        return ret

    def prepare(self, page, content):

        config = bconfig.load_config(None)
        title = config.get('title')
        if not title:
            title = 'Brick Dashboard'

        content = content.replace('__PANEL_TITLE__', title)
        return content.replace('__CONFIG__', str(config))

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'js'
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'css'
        },
        '/images': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'images'
        },
        '/help.html': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.getcwd() + '/templates/help.html'
        }
    }
    
    webapp = App()
    webapp.config = ConfigParser.ConfigParser()
    webapp.config.read('./app.cnf')
    cherrypy.quickstart(webapp, '/', conf)
