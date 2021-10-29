from flask_restx import Resource
from app import api, models_dao
import logging

log = logging.getLogger(__name__)


@api.route('/api/ml_models')
class MLModels(Resource):

    def get(self):
        return models_dao.ml_models

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass



@api.route('/api/ml_model/<int:id>')
class MLModel(Resource):

    def get(self, id):
        log.info(f'id = {id}\n type(id) = {type(id)}')
        try:
            return models_dao.get(id)
        except NotImplementedError as e:
            api.abort(404, e)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
