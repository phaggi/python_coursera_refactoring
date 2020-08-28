#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  task - refactoring

import math
import unittest

# =======================================================================================
# Функции для работы с векторами
# =======================================================================================
class Vec2d():
    '''
    Инициализируется вектором x(_, _).
    методы для основных математических операций, необходимых для работы с вектором:
    Vec2d.__add__ (сумма), Vec2d.__sub__ (разность), Vec2d.__mul__ (произведение 
    на число).
    Произведение на число может принимать число k.
    Есть возможность вычислять длину вектора с использованием функции len(a) 
    и метод int_pair, который возвращает кортеж из двух целых чисел 
    (текущие координаты вектора).
    '''
    def __init__(self, coord):
        self.coord = coord
    
    def __add__(self, y):
        '''
        переопределяет переопределяет оператор сумму для двух векторов
        '''
        return Vec2d((self.coord[0] + y.coord[0], self.coord[1] + y.coord[1]))
    
    def sub(self, a, b):
        '''
        вычисляет разность для двух векторов (внутренняя функция)
        '''
        return a[0] - b[0], a[1] - b[1]
    
    def __sub__(self, y):
        '''
        переопределяет оператор разность для двух векторов
        '''
        return Vec2d((self.sub(self.coord, y.coord)))
    
    def __mul__(self, k):
        return Vec2d((self.coord[0] * k, self.coord[1] * k))
    
    def __len__(self):
        return int(math.sqrt(float(self.coord[0] * self.coord[0] + self.coord[1] * self.coord[1])))
    
    def int_pair(self, y=None):
        '''
        возвращает пару координат, определяющих вектор (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с началом системы координат (0, 0)
        '''
        if y is None:
            y = Vec2d((0, 0))
        else:
            y = y
        return self.sub(y.coord, self.coord)
    
    '''    def __repr__(self):
        return repr(self.coord)'''

    def __str__(self):
        return str(self.coord)

class TestAll(unittest.TestCase):
    def test_Vec2d(self):
        ''' Проверяет, что класс Vec2d возвращает правильные значения.
            Для сравнения функции, которые были раньше вместо класса.
        '''
        self.cases = [[(1, 1),(2, 3), 0], 
                      [(222, 222),(111, 0), 1], 
                      [(0, 0),(-55, -99), 2],
                      [(-1, -1),(-55, -99), -2],
                      [(-1.1, -1.1),(55.555, -99.999), -2.001],
                      [(0, 0), (0, 0), 0]
                     ]
        def sub(x, y):
            """"возвращает разность двух векторов"""
            return x[0] - y[0], x[1] - y[1]


        def add(x, y):
            """возвращает сумму двух векторов"""
            return x[0] + y[0], x[1] + y[1]


        def length(x):
            """возвращает длину вектора"""
            return math.sqrt(x[0] * x[0] + x[1] * x[1])


        def mul(v, k):
            """возвращает произведение вектора на число"""
            return v[0] * k, v[1] * k


        def vec(x, y):
            """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
            координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
            return sub(y, x)

        for case in self.cases:
            
            x = case[0]
            y = case[1]
            k = case[2]
            vx = Vec2d(x)
            vy = Vec2d(y)
            self.assertEqual(str(add(x, y)), str(vx + vy))
            self.assertEqual(str(sub(x, y)), str(vx - vy))
            self.assertEqual(str(mul(x, k)), str(vx * k))
            self.assertEqual(int(length(x)), len(Vec2d(x)))
            self.assertEqual(vec(x, y), vx.int_pair(vy))
# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    unittest.main(argv=['ignored_arg'], exit=False)
 
