from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

# какую сущность мы ожидаем от клиента
# больше инфа для того, кто будет читать код, тк наш api примет на вход все (все что можно запихнуть в json)
ml_models_descr = api.model('ML models', {'id': fields.Integer,
                                          'name': fields.String,
                                          'accuracy': fields.Float})


class MLModelsDAO:
    def __init__(self):
        self.ml_models = [{'id': 1, 'name': 'logreg', 'accuracy': 0.77},
                          {'id': 2, 'name': 'tree', 'accuracy': 0.8}]
        self.counter = 2

    def get(self, id):
        for model in self.ml_models:
            if model['id'] == id:
                return model
        api.abort(404, 'ml_model {} doesnt exist'.format(id))

    def create(self, data):
        ml_model = data
        self.counter += 1
        ml_model['id'] = self.counter
        self.ml_models.append(ml_model)
        return ml_model

    def update(self, id, data):
        ml_model = self.get(id)
        ml_model.update(data)
        return ml_model

    def delete(self, id):
        ml_model = self.get(id)
        self.ml_models.remove(ml_model)


models_dao = MLModelsDAO()


@api.route('/api/ml_models')
class MLModels(Resource):

    def get(self):
        return models_dao.ml_models

    # нужно проверить то, что отдает клиент, на валидность
    @api.expect(ml_models_descr)
    def post(self):
        return models_dao.create(api.payload)


# пишем отдельный класс, поскольку переопределить мы их не можем
@api.route('/api/ml_models/<int:id>')
class MLModelsID(Resource):

    @api.expect(ml_models_descr)
    def put(self, id):
        models_dao.update(id, api.payload)

    @api.expect(ml_models_descr)
    def delete(self, id):
        models_dao.delete(id)
        return '', 204


if __name__ == '__main__':
    app.run()
