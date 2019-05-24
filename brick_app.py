import cherrypy
import os, tempfile, sys, socket, re
import configparser, importlib
from io import StringIO

sys.path.append("./modules")
import util, bconfig, brick

server_config = {
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 4443,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate':'/home/y/conf/sslcerts/server.crt',
    'server.ssl_private_key':'/home/y/conf/sslcerts/server.key',
    'server.ssl_certificate_chain':'/home/y/conf/sslcerts/server.intermediate.crt',
    'response.timeout': 10*60
}

# stag_server_config = {
#     'server.socket_host': '0.0.0.0',
#     'server.socket_port': 4443,
#     'response.timeout': 10*60
# }

cherrypy.config.update(server_config)

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
            return open('./templates/help.html')
        else:
            content = "".join(open('./templates/index.html').readlines())
            ret = self.prepare(args.get('page'), content)
            return ret.encode('utf-8')

    @cherrypy.expose
    @cherrypy.tools.jsonify()
    def query(self, **args):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        access, userid = self.permission_check()
        if not access:
            return {'error': "".join(open('./templates/help.html').readlines())}
        else:
            return self.process(args).encode('utf-8')
    
    def process(self, args):
        action = args.get('action')
        
        result = brick.execute(self.config, action, args)
        
        ret = util.json_to_str(result)
        print(ret[:1000])
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
        },
        '/status.html': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': '/home/y/share/htdocs/status.html'
        }
    }
    

    webapp = App()
    webapp.config = configparser.ConfigParser()
    webapp.config.read('./app.cnf')
    cherrypy.quickstart(webapp, '/', conf)
