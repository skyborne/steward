import falcon
import json

import server

api = falcon.API()

class UniqueIdentifierResource:
    def on_get(self, req, resp):
        resp.body = json.dumps({ 'id': str(server.generate_key()) })

class InformationResultsResource:
    def on_get(self, req, resp):
        resp.body = server.serve(req.params["id"])

api.add_route('/v1/keygen', UniqueIdentifierResource())
api.add_route('/v1/results', InformationResultsResource())
