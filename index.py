import falcon
import json

import server

api = falcon.API()

class UniqueIdentifierResource:
    def on_get(self, req, resp):
        identifier = { 'id': str(server.generate_key()) }

        resp.body = json.dumps(identifier)

api.add_route('/identifier', UniqueIdentifierResource())
