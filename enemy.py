import os
from pathlib import Path

from PyQt5.QtGui import QColor, QMovie
from PyQt5.QtWidgets import QLabel

import map
from bonus import Bonus
from constants import LIST_ENEMY, LIST_DIRECTION, SET_BONUS, COLOR_RED
import constants
import random

from player import Player


def fill_list_enemy(screen):
    """
    Метод заполняет карту врагами.
    :return:
    """
    LIST_ENEMY.append(Lower([1, 5], screen))
    LIST_ENEMY.append(Lower([6, 3], screen))
    LIST_ENEMY.append(Lower([1, 11], screen))
    LIST_ENEMY.append(Upper([10, 6], screen))

    # Кривовато


class Enemy:
    """
      Класс реализующий объект Enemy (базовый объект). Содержит все методы и свойства описывающие поведения Enemy.
    """
    def __init__(self, now_direction='left', old_direction='right', color=QColor(255, 255, 255), step=1, hit_point=1,
                 *__args):
        super().__init__(*__args)
        self.screen = None
        self.now_direction = now_direction
        self.old_direction = old_direction
        self.color = color
        self.step = step
        self.movie = None
        self.hit_point = hit_point

    def choose_direction(self):
        """
        Метод выбора случайного направления для движения.
        :return: None
        """
        maybe_new_direction = LIST_DIRECTION[random.randint(0, 3)]

        #   if (maybe_new_direction == 'left' and self.old_direction == 'right') or\
        #       (maybe_new_direction == 'right' and self.old_direction == 'left') or \
        #      (maybe_new_direction == 'up' and self.old_direction == 'down') or \
        #     (maybe_new_direction == 'down' and self.old_direction == 'up'):
        #   maybe_new_direction = list_direction[random.randint(0, 3)]
        #  Вариант с обходом.

        self.try_move(maybe_new_direction)

    def try_move(self, direction):
        """
        Метод пытается переместить Enemy по направлению direction с помощью метода map.can_move.
        Если map.can_move вернёт True, то заменяем объект по направлению direction на Enemy и делаем пустой
        позицию где стоял Enemy.
        :param direction: Параметр принимает направление, куда двигается Enemy.
        :return: None
        """
        new_position = list(self.position)

        if direction == 'left':
            new_position[0] -= self.step
        elif direction == 'right':
            new_position[0] += self.step
        elif direction == 'down':
            new_position[1] += self.step
        elif direction == 'up':
            new_position[1] -= self.step

        if not map.can_move(new_position):
            # Короче, если моб попадает в 'ловушку' пускай умирает, чтобы небыло рекурсии*
            try:
                self.choose_direction()
            except RecursionError:
                self.death()

            return

        if isinstance(map.get_object(self.position), Enemy):
            map.set_object(self.position, None)

        if not isinstance(map.get_object(new_position), Player):
            map.set_object(new_position, self)

        self.position = new_position    # узанть почему подчёркивает.

        return True

    def give_damage(self, damage_point):
        """
        Метод получения урона.
        :param damage_point: Параметр кол-ва урона.
        :return: None
        """
        self.hit_point -= damage_point

    def death(self):
        """
        Метод смерти и дропа Bonus после смерти, если это последний монстр на карте, дроп партала на сл. уровень.
        :return: None
        """
        map.set_object(self.position, None)
        constants.LIST_ENEMY.remove(self)
        if len(constants.LIST_ENEMY) == 0:
            self.end_lvl()
        else:
            bonus = Bonus(self.position)
            map.set_object(self.position, bonus)
            constants.SET_BONUS.add(bonus)
            if  self.screen:
                self.anime_enemy.clear()

    def end_lvl(self):
        """
        Метод создания партала для перехода на сл. уровень.
        :return: None
        """
        bonus = Bonus(self.position, portal=True, color=QColor(*COLOR_RED))
        map.set_object(self.position, bonus)
        constants.SET_BONUS.add(bonus)


class Lower(Enemy):
    """
      Класс реализующий объект Lower. Содержит все методы описывающие поведения Enemy и свойства Lower.
    """
    def __init__(self, position, screen=None, color=QColor(55, 228, 255)):
        super().__init__()
        self.screen = screen
        self.position = position
        self.color = color
        self.hit_point = 1
        if screen:
            self.movie = QMovie(os.path.join('gif', 'enemy.gif'))
            self.movie.start()
            self.anime_enemy = QLabel(screen)


class Upper(Enemy):
    """
      Класс реализующий объект Upper. Содержит все методы описывающие поведения Enemy и свойства Upper.
    """
    def __init__(self, position, screen=None, color=QColor(228, 55, 255)):
        super().__init__()
        self.position = position
        self.screen = screen
        self.color = color
        self.hit_point = 2
        if screen:
            self.movie = QMovie(os.path.join('gif', 'enemy2.gif'))
            self.movie.start()
            self.anime_enemy = QLabel(screen)


