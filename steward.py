import falcon
import json

import helper

api = falcon.API()

class UniqueIdentifierResource:
    def on_get(self, req, resp):
        resp.body = helper.generate_key()

class InformationResultsResource:
    def on_get(self, req, resp):
        resp.body = helper.serve(req.params["id"])

api.add_route('/v1/keygen', UniqueIdentifierResource())
api.add_route('/v1/results', InformationResultsResource())
