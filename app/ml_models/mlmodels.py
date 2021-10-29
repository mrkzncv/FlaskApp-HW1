import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVR, SVC
from sklearn.model_selection import GridSearchCV


class MLModelsDAO:
    def __init__(self, ):
        self.ml_models = []
        self.counter = 0

    def get(self, id):
        """
        Функция обучает модель с заданным id и выдает предсказания
        :param id: integer: уникальный идентификатор модели
        :return: list: предсказания модели
        """
        for model in self.ml_models:
            if model['id'] == id:
                f_name = f"models static/{model['problem']}_{model['name']}_{model['id']}.pickle"
                trained_model = pickle.load(open(f_name, 'rb'))
                prediction = trained_model.predict(np.array(model['X']))
                return prediction.tolist()

        raise NotImplementedError('ml_model {} does not exist'.format(id))

    def create(self, data, is_new=True):  # пришли данные, надо присвоить id (для POST)
        """
        Обучение (переобучение) модели. На вход подается запрос на обучение модели и данные.
        Если у нас предусмотрена запрашиваемая функциональность, модель обучается и записывается в pickle
        с id модели в названии файла. Путь до файла записывается в json с ключом 'model_path'.
        :param data: json {'problem': 'classification', 'name': 'Random Forest', 'h_tune': False, 'X':x, 'y':y}
        :param is_new: boolean: новая ли модель или надо переобучать существующую
        :return: список обученных моделей
        """
        ml_model = data
        if (ml_model['problem'] in ['classification', 'regression']) and \
                (ml_model['name'] in ['Random Forest', 'SVM']):
            if is_new:
                self.counter += 1
                ml_model['id'] = self.counter
            x, y = np.array(ml_model['X']), np.array(ml_model['y'])
            if ml_model['problem'] == 'classification':
                best_model = self.classification(ml_model['name'], x, y, h_tune=ml_model['h_tune'])
                f_name = f"models static/{ml_model['problem']}_{ml_model['name']}_{ml_model['id']}.pickle"
                pickle.dump(best_model, open(f_name, 'wb'))
                ml_model['model_path'] = f_name
            elif ml_model['problem'] == 'regression':
                best_model = self.regression(ml_model['name'], x, y, h_tune=ml_model['h_tune'])
                f_name = f"models static/{ml_model['problem']}_{ml_model['name']}_{ml_model['id']}.pickle"
                pickle.dump(best_model, open(f_name, 'wb'))
                ml_model['model_path'] = f_name
            if is_new:
                self.ml_models.append(ml_model)
        else:
            raise NotImplementedError("""Сейчас доступны для обучения только classification and regression:
                                        Random Forest или SVM""")
        return ml_model

    def update(self, id, data):
        """
        Функция либо переобучает модель, либо выдает ошибку, что такой модели ещё нет, надо создать новую
        :param id: integer: уникальный идентификатор модели
        :param data: json с новыми параметрами для модели
        :return: ничего не выдает
        """
        ml_model = None
        for model in self.ml_models:
            if model['id'] == id:
                ml_model = model  # json со старыми параметрами
        if ml_model is None:
            raise NotImplementedError('Такой модели ещё нет, надо создать новую')
        else:
            if (data['name'] == ml_model['name']) and (data['problem'] == ml_model['problem']):
                ml_model.update(data)  # кладу в них новые данные, 'X', 'y', 'h_tune'
                self.create(ml_model, is_new=False)  # переобучаю модель
            else:
                raise NotImplementedError('Такой модели ещё нет, надо создать новую')

    def delete(self, id):
        """
        Удаление модели по id
        :param id: integer: уникальный идентификатор модели
        :return: удаление модели из списка моделей
        """
        for model in self.ml_models:
            if model['id'] == id:
                self.ml_models.remove(model)

    @staticmethod
    def classification(model, x, y, h_tune=False):
        """
        :param model: название класса для модели классификации (строка) - "Random Forest" или "SVM".
        :param x: np.array(): выборка с признаками для обучения.
        :param y: np.array(): таргеты.
        :param h_tune: boolean: нужен ли подбор гиперпараметров или нет.
        :return: model(): обученная модель.
        """
        if model == 'Random Forest':
            param_grid = {'n_estimators': [50, 100], 'max_depth': [3, 4], 'max_features': ['auto', 'sqrt']}
            clf = RandomForestClassifier(random_state=0)
        elif model == 'SVM':
            param_grid = {'kernel': ('linear', 'rbf'), 'C': [1, 10]}
            clf = SVC(random_state=0)

        if h_tune:
            clf_cv = GridSearchCV(estimator=clf, param_grid=param_grid, cv=5)
            clf_cv.fit(x, y)
            return clf_cv.best_estimator_
        else:
            clf.fit(x, y)
            return clf

    @staticmethod
    def regression(model, x, y, h_tune=False):
        """
        :param model: название класса для модели регрессии (строка) - "Random Forest" или "SVM".
        :param x: np.array(): выборка с признаками для обучения.
        :param y: np.array(): таргеты.
        :param h_tune: boolean: нужен ли подбор гиперпараметров или нет.
        :return: model(): обученная модель.
        """
        if model == 'Random Forest':
            param_grid = {'n_estimators': [50, 100], 'max_depth': [3, 4], 'max_features': ['auto', 'sqrt']}
            lr = RandomForestRegressor(random_state=0)
        elif model == 'SVM':
            param_grid = {'kernel': ('linear', 'rbf'), 'C': [1, 10]}
            lr = SVR()

        if h_tune:
            lr_cv = GridSearchCV(estimator=lr, param_grid=param_grid, cv=5)
            lr_cv.fit(x, y)
            return lr_cv.best_estimator_

        else:
            lr.fit(x, y)
            return lr
