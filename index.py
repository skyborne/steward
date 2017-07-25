import falcon
import json

import server

api = falcon.API()

class UniqueIdentifierResource:
    def on_get(self, req, resp):
        resp.body = json.dumps({ 'id': str(server.generate_key()) })

class InformationResultsResource:
    def on_get(self, req, resp):
        fwd = "Fwd: "
        params = req.params
        uuid = params["uuid"]

        subject = fwd + uuid

        resp.body = server.serve(subject)
        # resp.body = server.serve('Fwd: f9231901-e32e-463d-a1e2-6694fb63e0c8')

api.add_route('/uuid', UniqueIdentifierResource())
api.add_route('/mail', InformationResultsResource())
