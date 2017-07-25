import falcon
import json

import server

api = falcon.API()

class UniqueIdentifierResource:
    def on_get(self, req, resp):
        resp.body = json.dumps({ 'id': str(server.generate_key()) })

api.add_route('/identifier', UniqueIdentifierResource())

class InformationResultsResource:
    def on_get(self, req, resp):
        resp.body = server.serve('Fwd: f9231901-e32e-463d-a1e2-6694fb63e0c8')

api.add_route('/results', InformationResultsResource())
