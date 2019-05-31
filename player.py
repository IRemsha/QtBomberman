import os
from pathlib import Path

from PyQt5.QtGui import QColor, QMovie
from PyQt5.QtWidgets import QLabel

from bomb import SimpleBomb, Mine
import constants
import map


class Player:
    """
    Класс реализующий объект Player. Содержит все методы и свойства описывающие поведения Player.
    """
    def __init__(self, position, screen=None, color=QColor(255, 228, 181), step=1, hit_point=1, power_bomb=1, count_bomb=2,
                 type_bomb=0, coef_speed_enemy=0.5):
        self.position = position
        self.screen = screen
        self.color = color
        self.step = step
        self.hit_point = hit_point
        self.power_bomb = power_bomb
        self.count_bomb = count_bomb
        self.type_bomb = type_bomb
        self.anim_left = False
        self.anim_right = False
        self.anim_up = False
        self.anim_down = False
        self.anim_dmg = False
        self.coef_speed_enemy = coef_speed_enemy

    def move(self, direction):
        """
        Метод принимает сигнал от нажаткой клав, создаёт координату, куда хочет перейти игрок и проверяет возможно ли
        это сделать.
        :param direction: Параметр сигнала (нажатая клав.) - направление.
        :return: None
        """
        maybe_new_position = list(self.position)
        if direction == 'left':
            maybe_new_position[0] -= self.step
        elif direction == 'right':
            maybe_new_position[0] += self.step
        elif direction == 'up':
            maybe_new_position[1] -= self.step
        elif direction == 'down':
            maybe_new_position[1] += self.step
        else:
            return

        self.try_move(maybe_new_position)

    def try_move(self, new_position):
        """
        Метод пытается переместить Player на координату new_position с помощью метода map.can_move.
        Если map.can_move вернёт True, то заменяем объект по координате new_position на Player и делаем пустой
        позицию где стоял Player.
        :param new_position: Параметр принимает координату, куда хочет перейти Player.
        :return: None
        """
        if not map.can_move(new_position):
            return

        if isinstance(map.get_object(self.position), Player):
            map.set_object(self.position, None)
        map.set_object(new_position, self)
        if self.screen:
            self.screen.anime_player3(self.position, new_position)
        self.position = new_position

    def drop_bomb(self):
        """
        Метод установки бомбы.
        :return: None
        """
        if isinstance(map.get_object(self.position), Player) and self.count_bomb > 0.9:
            if self.type_bomb == 0:
                is_bomb = SimpleBomb(self.position, self, self.power_bomb, screen=self.screen)
            else:
                is_bomb = Mine(self.position, self, screen=self.screen)
            constants.SET_BOMBS.add(is_bomb)
            map.set_object(self.position, is_bomb)
            self.count_bomb -= 1
            print('Осталось: {} бомб(ы)'.format(self.count_bomb))
        else:
            return

    def refresh_bomb(self):
        """
        Метод пополенения запаса бомб.
        :return: None
        """
        self.count_bomb += 1

    def change_type_bomb(self):
        """
        Метод - хезе что за метод.
        :return: None
        """
        pass

    def give_damage(self, damage_point):
        """
        Метод получения урона.
        :param damage_point: Параметр кол-ва урона.
        :return: None
        """
        self.hit_point -= damage_point

    def death(self):
        """
        Метод смерти.
        :return: None
        """
        map.set_object(self.position, None)
        self.color = QColor(128, 128, 128)

    def get_bonus(self):
        """
        Метод получения Bonus.
        :return: None
        """
        if self.coef_speed_enemy > 0.1:
            self.coef_speed_enemy -= 0.01
        else:
            self.coef_speed_enemy = 0.05

        self.count_bomb += 0.5

    def roll_bomb(self):
        """
        Метод изменения типа бомбы в руке у Player
        :return: None
        """
        if self.type_bomb == 0:
            self.type_bomb = 1
        else:
            self.type_bomb = 0


