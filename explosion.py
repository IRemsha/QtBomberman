from pathlib import Path

from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel
import os
from constants import SET_EXPLOSIONS
import map


class Explosion:
    """
      Класс реализующий объект Explosion. Содержит все методы и свойства описывающие Explosion.
    """
    def __init__(self, position, bomb, screen, timer=3):
        self.position = position
        self.screen = screen
        self.bomb = bomb
        self.timer = timer
        self.movie = QMovie(os.path.join('gif', 'expl.gif'))
        self.movie.start()
        self.anime_expl = QLabel(screen)

    def explosion_region(self):
        """
        Знакомьтесь, плохой метод.
        Метод фиксирующий область взрыва бомбы.
        :return: None
        """
        expl_left = Explosion([self.position[0] - 1, self.position[1]], self.bomb, self.screen)
        expl_right = Explosion([self.position[0] + 1, self.position[1]], self.bomb, self.screen)
        expl_up = Explosion([self.position[0], self.position[1] - 1], self.bomb, self.screen)
        expl_down = Explosion([self.position[0], self.position[1] + 1], self.bomb, self.screen)

        if map.get_visible(self.position).is_destroyable():
            SET_EXPLOSIONS.add(self)
        if map.get_visible(expl_right.position).is_destroyable():
            SET_EXPLOSIONS.add(expl_right)
        if map.get_visible(expl_left.position).is_destroyable():
            SET_EXPLOSIONS.add(expl_left)
        if map.get_visible(expl_up.position).is_destroyable():
            SET_EXPLOSIONS.add(expl_up)
        if map.get_visible(expl_down.position).is_destroyable():
            SET_EXPLOSIONS.add(expl_down)

        self.blow_up()

    def ticker(self):
        """
        Метод - счётчик для взрыва, если счётчик 0 - взрыв исчезает.
        :return: None
        """
        self.timer -= 1
        if self.timer < 0:
            SET_EXPLOSIONS.discard(self)
            self.anime_expl.clear()
        else:
            return

    def blow_up(self):
        """
        Метод подрыва объектов на карте, нанести урон всем, кто попал в область поражения.
        :return: None
        """
        for explosion in SET_EXPLOSIONS.copy():
            map.blow_up_block(explosion.position)
            map.damage_bomb(explosion.position, self.bomb.power_bomb)

