# -*- coding: utf-8 -*-

import numpy as np
from scipy import special
from sklearn.base import ClassifierMixin, BaseEstimator
from sklearn.datasets import make_classification

# Используйте scipy.special для вычисления численно неустойчивых функций
# https://docs.scipy.org/doc/scipy/reference/special.html#module-scipy.special

def lossf(w, X, y, l1, l2):
    """
    Вычисление функции потерь.

    :param w: numpy.array размера  (M,) dtype = np.float
    :param X: numpy.array размера  (N, M), dtype = np.float
    :param y: numpy.array размера  (N,), dtype = np.int
    :param l1: float, l1 коэффициент регуляризатора 
    :param l2: float, l2 коэффициент регуляризатора 
    :return: float, значение функции потерь
    """
    # Вам необходимо вычислить значение функции потерь тут, решение может занимать 1 строку
    lossf = sum(np.logaddexp(np.zeros_like(y), -np.dot(X,w) * y ) ) * 1.0 + (np.linalg.norm(w)) * l1 * 1.0 + (np.linalg.norm(w) ** 2) * l2 * 1.0
    return lossf

def gradf(w, X, y, l1, l2):
    """
    Вычисление градиента функции потерь.

    :param w: numpy.array размера  (M,), dtype = np.float
    :param X: numpy.array размера  (N, M), dtype = np.float
    :param y: numpy.array размера  (N,), dtype = np.int
    :param l1: float, l1 коэффициент регуляризатора 
    :param l2: float, l2 коэффициент регуляризатора 
    :return: numpy.array размера  (M,), dtype = np.float, градиент функции потерь d lossf / dw
    """
    gradw = np.zeros(len(w))# Вам необходимо вычислить градиент функции потерь тут, решение может занимать 1 строку
    w_1 = [1.0 if i >= 0 else -1.0 for i in range(len(w))]
    w_1 = np.array(w_1)
    gradw = np.dot(special.expit(-np.dot(X, w) * y), (-y * X.T).T )+ w_1 * l1 + w * 2.0 * l2
    return gradw

class LR(ClassifierMixin, BaseEstimator):
    def __init__(self, lr=1, l1=1e-4, l2=1e-4, num_iter=1000, verbose=0):
        """
        Создание класса для лог регрессии
        
        :param lr: float, длина шага для оптимизатора
        :param l1: float, l1 коэффициент регуляризатора 
        :param l2: float, l2 коэффициент регуляризатора
        :param num_iter: int, число итераций оптимизатора
        :param verbose: bool, ключик для вывода
        """
        self.l1 = l1
        self.l2 = l2
        self.w = None
        self.lr = lr
        self.verbose = verbose
        self.num_iter = num_iter

    def fit(self, X, y):
        """
        Обучение логистической регрессии.
        Настраивает self.w коэффициенты модели.

        Если self.verbose == True, то выводите значение 
        функции потерь на итерациях метода оптимизации. 

        :param X: numpy.array размера  (N, M), dtype = np.float
        :param y: numpy.array размера  (N,), dtype = np.int
        :return: self
        """
        n, d = X.shape
        self.w = np.ones(d)# Задайте начальное приближение вектора весов
        # Настройте параметры функции потерь с помощью градиентного спуска
        for i in range(self.num_iter):
            if self.verbose:
                print lossf(self.w, X, y, self.l1, self.l2)
            self.w = self.w + self.lr * gradf(self.w, X, y, self.l1, self.l2)
        return self

    def predict_proba(self, X):
        """
        Предсказание вероятности принадлежности объекта к классу 1.
        Возвращает np.array размера (N,) чисел в отрезке от 0 до 1.

        :param X: numpy.array размера  (N, M), dtype = np.float
        :return: numpy.array размера  (N,), dtype = np.float
        """
        # Вычислите вероятности принадлежности каждого 
        # объекта из X к положительному классу, используйте
        # эту функцию для реализации LR.predict
        probs = special.expit(np.dot(X, self.w)) * 1.0
        return probs

    def predict(self, X):
        """
        Предсказание класса для объекта.
        Возвращает np.array размера (N,) элементов 1 или -1.

        :param X: numpy.array размера  (N, M), dtype = np.float
        :return:  numpy.array размера  (N,), dtype = np.int
        """
        # Вычислите предсказания для каждого объекта из X
        preds = -np.sign(np.dot(X, self.w))
        return preds

def test_work():
    print "Start test"
    X, y = make_classification(n_features=100, n_samples=1000)
    y = 2 * (y - 0.5)
    try:
        clf = LR(lr=1e-3, l1=1e-4, l2=1e-4, num_iter=100, verbose=0)
    except Exception:
        assert False, "Создание модели завершается с ошибкой"
        return

    try:
        clf = clf.fit(X, y)
    except Exception:
        assert False, "Обучение модели завершается с ошибкой"
        return
    assert isinstance(lossf(clf.w, X, y, 1e-3, 1e-3), float), "Функция потерь должна быть скалярной и иметь тип np.float"
    assert gradf(clf.w, X, y, 1e-3, 1e-3).shape == (100,), "Размерность градиента должна совпадать с числом параметров"
    assert gradf(clf.w, X, y, 1e-3, 1e-3).dtype == np.float, "Вектор градиента, должен состоять из элементов типа np.float"
    assert clf.predict(X).shape == (1000,), "Размер вектора предсказаний, должен совпадать с количеством объектов"
    assert np.min(clf.predict_proba(X)) >= 0, "Вероятности должны быть не меньше, чем 0"
    assert np.max(clf.predict_proba(X)) <= 1, "Вероятности должны быть не больше, чем 1"
    assert len(set(clf.predict(X))) == 2, "Метод предсказывает больше чем 2 класса на двух классовой задаче"
    print "End tests"

test_work()
