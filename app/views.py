from flask_restx import Resource, fields
from app import api, models_dao
import logging

log = logging.getLogger(__name__)

# шаблон с описанием сущности
# ml_models_desc = api.model('ML models', {'id': fields.Integer,
#                                          'problem': fields.String,
#                                          'name': fields.String,
#                                          # 'accuracy': fields.Float,
#                                          'h_tune': fields.Boolean,
#                                          'X': fields.List,  # ??
#                                          'y': fields.List,  # ??
#                                          'h_params': fields.List,
#                                          'prediction': fields.List})

implemented_models = {'classification': ['Random Forest', 'SVM'],
                      'regression': ['Random Forest', 'SVM']}


@api.route('/api/ml_models')
class MLModels(Resource):

    @staticmethod
    def get(self):
        """
        Возвращает доступные классы и информацию об обученных моделях.
        """
        return [implemented_models, models_dao.ml_models]

    @staticmethod
    # @api.expect(ml_models_desc) # нужно проверить то, что отдает клиент, на валидность
    def post(self):
        """
        Обучение новой модели.
        """
        return models_dao.create(api.payload)

    def put(self):  # update?
        pass

    def delete(self):
        pass


@api.route('/api/ml_models/<int:id>')
class MLModelsID(Resource):

    @staticmethod
    def get(self, id):
    # log.info(f'id = {id}\n type(id) = {type(id)}')
        try:
            return models_dao.get(id)
        except NotImplementedError as e:
            api.abort(404, e)

    @staticmethod
    # @api.expect(ml_models_desc)
    def put(self, id):  # update
        """
        Переобучение модели на новых данных по id.
        """
        return models_dao.update(id, api.payload)

    @staticmethod
    # @api.expect(ml_models_desc)
    def delete(self, id):
        """
        Удаление данных о модели.
        """
        models_dao.delete(id)
        return '', 204

