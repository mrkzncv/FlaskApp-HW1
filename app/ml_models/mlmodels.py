class MLModelsDAO:
    def __init__(self, ):
        self.ml_models = [{'id': 1, 'name': 'logreg', 'acc': 0.7},
                          {'id': 2, 'name': 'DT', 'acc': 0.8}]
        self.counter = 2

    def get(self, id):
        for model in self.ml_models:
            if model['id'] == id:
                return model
        raise NotImplementedError('ml_model {} doesnot exist'.format(id))