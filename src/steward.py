import falcon
import json

import helper

api = falcon.API()


class UniqueIdentifierResource:
    def on_get(self, req, resp):
        resp.body = helper.generate_key()


class InformationResultsResource:
    def on_get(self, req, resp):
        response = helper.serve(req.params["id"])
        if response:
            if json.loads(response).get('result'):
                resp.body = response

        if resp.body is None:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = json.dumps({'error': 'invalid'}, indent=2)


api.add_route('/v1/keygen', UniqueIdentifierResource())
api.add_route('/v1/results', InformationResultsResource())
