import os
from pathlib import Path

from PyQt5.QtGui import QColor, QMovie
from PyQt5.QtWidgets import QLabel

import map
from constants import SET_BOMBS
import constants
from explosion import Explosion


class Bomb:
    """
    Класс реализующий объект Bomb. Содержит все методы и свойства описывающие Bomb.
    """
    def __init__(self):
        self.screen = None
        self.player = None
        self.position = None
        self.color = QColor(128, 0, 0)
        self.timer = 10
        self.anim = False
        self.assets = True

    def ticker(self):
        """
        Метод - счётчик для бомбы, если счётчик 0 - вызывает Boom
        :return: None
        """
        self.timer -= 1
        if self.timer < 0:
            self.boom()
        else:
            return

    def boom(self):
        """
        Метод - взрыв бомбы.
        :return: None
        """
        is_explosion = Explosion(self.position, self, screen=self.screen)
        is_explosion.explosion_region()
        #   print('Взрыв')
        self.remove() # ремув будет в map при удалении блока == бромбы

    def remove(self):
        """
        Метод удаляет бомбу из Множества бомб и Объектной карты после взрыва.
        :return: None
        """
        map.set_object(self.position, None)
        constants.SET_BOMBS.discard(self)
        if self.screen:
            self.anime_bomb.clear()

        self.player.refresh_bomb()


class SimpleBomb(Bomb):
    """
    Класс реализующий объект SimpleBomb. Содержит методы Bomb и свойства SimpleBomb.
    """
    def __init__(self, position, player, power_bomb, screen=None):
        super().__init__()
        self.screen = screen
        self.movie = QMovie(os.path.join('gif', 'bomb.gif'))
        self.movie.start()
        self.anime_bomb = QLabel(screen)
        self.position = position
        self.player = player
        self.power_bomb = power_bomb
        self.color = QColor(255, 46, 0)
        self.timer = 5


class Mine(Bomb):
    """
    Класс реализующий объект GreenBomb. Содержит методы Bomb и свойства GreenBomb.
    (Урона больше)
    """
    def __init__(self, position, player, screen=None, power_bomb=2):
        super().__init__()
        self.screen = screen
        self.movie = QMovie(os.path.join('gif', 'mine.gif'))
        self.movie.start()
        self.anime_bomb = QLabel(screen)
        self.position = position
        self.player = player
        self.power_bomb = power_bomb
        self.color = QColor(0, 144, 0)
        self.assets = False
