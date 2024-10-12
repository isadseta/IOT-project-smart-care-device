
__requires__ = [
    'cherrypy_cors',
]

import cherrypy
import cherrypy_cors


class MyResource:

    @cherrypy.expose()
    def index(self):
        return '{"value": "success"}\n'

    @classmethod
    def run(cls):
        cherrypy_cors.install()
        config = {
            '/': {
                'cors.expose.on': True,
            },
        }
        cherrypy.quickstart(cls(), config=config)


__name__ == '__main__' and MyResource.run()