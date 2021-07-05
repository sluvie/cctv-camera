import os

path = os.path.abspath(os.path.dirname(__file__))
config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 3001,
        'server.thread_pool': 8,
        'engine.autoreload.on': True,
        'tools.trailing_slash.on': False
    },
    '/resources': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(path, 'assets', 'resources')
    },
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd())
    }
}