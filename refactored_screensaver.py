#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  task - refactoring

import pygame
import random
import math
import unittest

width = 1
color = (255, 255, 255)

# =======================================================================================
# Класс для работы с векторами
# =======================================================================================


# =======================================================================================
class Vec2d():
    '''
    Инициализируется вектором (_, _) или парой аргументов Vec2d(_, _)
    методы для основных математических операций, необходимых для работы с вектором:
    Vec2d.__add__ (сумма), Vec2d.__sub__ (разность), Vec2d.__mul__ (произведение 
    на число).
    Произведение на число может принимать число k.
    Есть возможность вычислять длину вектора с использованием функции len(a) 
    и метод int_pair, который возвращает кортеж из двух целых чисел 
    (текущие координаты вектора).
    '''
    def __init__(self, *args):
        if len(args) == 1 and type(args) is tuple and type(args[0]) is tuple and len(args[0]) == 2:
            self.coord = args[0]
        elif len(args) == 2 and type(args) is tuple and len(args) == 2:
            self.coord = args
        else:
            raise Exception('Wrong arguments')
    
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
    
    def int_pair(self):
        '''
        возвращает пару координат из двух целых чисел
        '''
        return (int(self.coord[0]), int(self.coord[1]))
    
    '''    def __repr__(self):
        return repr(self.coord)'''
    
    def vec(self, y=None):
        '''
        возвращает пару координат, определяющих вектор (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с началом системы координат (0, 0)
        '''
        if y is None:
            y = Vec2d((0, 0))
        else:
            y = y
        return self.sub(y.coord, self.coord)

    def __str__(self):
        return str(self.coord)

# =======================================================================================
# Класс точек
# =======================================================================================

class Point():
    def __init__(self, pointvect: Vec2d, speedvect: Vec2d):
        self.pointvect = pointvect
        self.speedvect = speedvect

    def set_point(self, screendim: tuple):
        '''
        функция перерасчета координаты опорной точки
        '''
        self.screendim = screendim
        self.pointvect += self.speedvect
        if int(self.pointvect.coord[0]) > self.screendim[0] or int(self.pointvect.coord[0]) < 0:
            self.speedvect -= Vec2d((self.speedvect.coord[0], 0)) * 2
        if int(self.pointvect.coord[1]) > self.screendim[1] or int(self.pointvect.coord[1]) < 0:
            self.speedvect -= Vec2d((0, self.speedvect.coord[1])) * 2
            
    def __str__(self):
        return str(str(self.pointvect) + ', ' + str(self.speedvect))


# =======================================================================================
# Класс кривой
# =======================================================================================

class Polyline():
    '''
    класс замкнутых ломаных Polyline с методами, отвечающими за добавление в ломаную 
    точки (Vec2d) c её скоростью, пересчёт координат точек (set_points) и отрисовку 
    ломаной (draw_points).
    Арифметические действия с векторами реализованы с помощью операторов, а не через 
    вызовы соответствующих методов.
    '''
    def __init__(self):
        self.points = list()
        self.polyline = list()
        try:
            self._steps = steps
        except NameError:
            self._steps = 35
        
    
    def make_point(self, _base_points, _alpha, _deg=None):
        '''
        def get_point(points, alpha, deg=None):
            if deg is None:
                deg = len(points) - 1
            if deg == 0:
                return points[0]
            return add(mul(points[deg], alpha), mul(get_point(points, alpha, deg - 1), 1 - alpha))
        '''
        if _deg is None:
                _deg = len(_base_points) - 1
        if _deg == 0:
                _point = _base_points[0]
        else:
            _maked_point =  self.make_point(_base_points, _alpha, _deg - 1)
            _point = _base_points[_deg] * _alpha + _maked_point * (1 - _alpha)
        return _point
    
    def make_points(self, _base_points: list):
        """
        def get_points(base_points, count):
            alpha = 1 / count
            res = []
            for i in range(count):
                res.append(get_point(base_points, i * alpha))
            return res
        """
        _points = []
        _alpha = 1 / self._steps
        for _i in range(self._steps):
            _points.append(self.make_point(_base_points, _i * _alpha))
        return _points

    def append(self, point):
        self.points.append(point)
    
    def set_points(self, screendim):
        """
        функция перерасчета координат опорных точек
        """
        self._screendim = screendim
        for _nextpoint in self.points:
            _nextpoint.set_point(self._screendim)

    def get_points_polyline(self):
        _result = []
        for point in self.points:
            _result.append(point.pointvect.coord)
        return _result
    
    def get_speeds_polyline(self):
        _result = []
        for point in self.points:
            _result.append(point.speedvect.coord)
        return _result
    
    def __str__(self):
        return str(self.points.get_points())
    
    def make_base_points(self, _num_point):
        """
        функция возвращает список с точками кривой для данной базовой точки
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append(mul(add(points[i], points[i + 1]), 0.5))
            ptn.append(points[i + 1])
            ptn.append(mul(add(points[i + 1], points[i + 2]), 0.5))
        """
        
        _base_points = list()
        
        _first_point = self.points[_num_point - 1].pointvect
        _next_point = self.points[_num_point].pointvect
        _base_points.append((_first_point + _next_point) * 0.5)
        
        _base_points.append(_next_point)
        
        _first_point = self.points[_num_point].pointvect
        _next_point = self.points[_num_point + 1].pointvect
        _base_points.append((_first_point + _next_point) * 0.5)
        
        return _base_points

    def make_polyline_list(self):
        """
        функция возвращает список с точками кривой на основании базовых точек self
        
        """
        _result = list()
        if len(self.points) >= 3:
            for _num_point in range(-2, len(self.points)-2):
                _base_points = self.make_base_points(_num_point)
                _points = self.make_points(_base_points)
                _result.extend(_points)
        return _result
    
    def draw_points(self, gamedisplay, color, radius, width):
        """
        функция отрисовки точек на экране
        """
        self._width = width
        self._color = color
        self._radius = radius
        self._gamedisplay = gamedisplay
        for _point in self.points:
            self._pointcoord = (int(_point.pointvect.coord[0]), int(_point.pointvect.coord[1]))
            pygame.draw.circle(self._gamedisplay, self._color, self._pointcoord, self._radius, self._width)

    def draw_lines(self, gamedisplay, color, width, steps):
        """
        функция отрисовки кривых из прямых на экране
        """
        self._width = width
        self._color = color
        self._gamedisplay = gamedisplay
        self._points = self.make_polyline_list()
        self._steps = steps
        if len(self._points) >= 3:
            self._first_point = self._points[len(self._points)-1].int_pair()
            for _next_point in self._points:
                self._next_point = _next_point.int_pair()
                pygame.draw.line(self._gamedisplay, self._color,
                        self._first_point, self._next_point, self._width)
                self._first_point = (self._next_point[0], self._next_point[1])

        

# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    
    screen_dim = (800, 600)
    speedup = (screen_dim[0] + screen_dim[1]) // 200

    P = Polyline()
    '''    points = [(10, 10), (20, 40), (100, 50)]
    for coord in points:
        speed = (random.random()  * speedup / 10, random.random()  * speedup / 10)
        P.append(Point(Vec2d(coord), Vec2d(speed)))'''

    pygame.init()
    gameDisplay = pygame.display.set_mode(screen_dim)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    show_help = False
    pause = True
    radius = 2
    hue = 0
    color = pygame.Color(0)
    point_color = (255, 255, 255)
    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    P = Polyline()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                newpoint = Vec2d(event.pos)
                newspeed = Vec2d((random.random() * speedup / 10, random.random() * speedup / 10))
                P.append(Point(newpoint, newspeed))
                hue = (hue + 10) % 360
        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        P.draw_points(gameDisplay, point_color, radius, width)
        P.draw_lines(gameDisplay, color, width, steps)
        if not pause:
            P.set_points(screen_dim)
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
