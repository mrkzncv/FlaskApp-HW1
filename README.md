__API предоставляет следующую функциональность:__
1) Обучение ML-моделей с возможностью настройки гиперпараметров.
2) Гиперпараметры для разных моделей могут быть разные.
3) Количество классов моделей доступных для обучения == 2. На данный момент программа позволяет решать задачи регрессии и классификации с помощью моделей Random Forest и SVM.

__Подбробное описание функций находится внутри файлов `mlmodels.py` и `views.py`__

__Запуск Api из командной строки:__

``python cli.py``

__Работа с Api:__

1. Общая информация по моделям:
``r_n = requests.get('http://192.168.1.12:5000/api/ml_models')``
- получить список моделей, доступных для обучения: ``r_n.json()[0]``
- получить список обученных моделей: ``r_n.json()[1]``
- id модели и пути, где они лежат:
``[s['model_path'] for s in r_n.json()[1]], [s['id'] for s in r_n.json()[1]]``
2. Получение предсказаний конкретной модели:

``prediction = requests.get('http://192.168.1.12:5000/api/ml_models/{id}').json()``
3. Обучение новой модели:
 ``data={'problem': 'classification', 'name': 'Random Forest', 'h_tune': False, 'X':X.tolist(), 'y':y.tolist()}``
 ``requests.post('http://192.168.1.12:5000/api/ml_models', json=data)``
 
   Параметры:
   - problem: 'classification', 'regression'
   - name: 'Random Forest', 'SVM'
   - h_tune: нужен ли подбор гиперпараметров (если нужен, выполняется GridSearch по фиксированной сетке)
   - X: список с фичами
   - y: список значений таргета
   
4. Удаление обученной модели:
``requests.delete('http://192.168.1.12:5000/api/ml_models/{id}')``
5. Переобучение модели:
``requests.put('http://192.168.1.12:5000/api/ml_models/4', json={'problem': 'classification', 'name': 'Random Forest', 'h_tune': True})``

Это релиз. При дальнейших доработках можно учесть:
- обработку ошибок при добавлении неверных типов данных, неподходящих под задачу
- реализовать возможность задания гиперпараметров
- возможность скачивания модели пользователем
- др.

