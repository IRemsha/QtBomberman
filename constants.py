import os
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox
import map

HEIGHT_BLOCK = 13
WIDTH_BLOCK = 13
SIZE_PIXEL_BLOCK = 50

BLOCK_EMPTY, BLOCK_WALL, BLOCK_BRICK = range(3)
SET_TYPE_BLOCK = [BLOCK_EMPTY, BLOCK_WALL, BLOCK_BRICK]

HEIGHT_MAP, WIDTH_MAP = HEIGHT_BLOCK * SIZE_PIXEL_BLOCK, WIDTH_BLOCK * SIZE_PIXEL_BLOCK

LIST_DIRECTION = ['left', 'right', 'up', 'down']
SET_BOMBS = set()
SET_EXPLOSIONS = set()
SET_BONUS = set()
LIST_PLAYERS = []
LIST_ENEMY = []

COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

MESSAGE_ERROR_LOAD_GAME = 'Сохранение на найдено & Загрузим обычную игру?'
MESSAGE_INFO_GAME = 'Управление= \n Передвижение: на стрелочки \n Ставить бомбу: ПРОБЕЛ \n Сменить бомбу: л.Shift' \
                    '\n Сохранить игру: S \n Загрузить игру: L \n HELP табличка: I \n Загрузить сл. уровень игры: N \n'\
                    '\nЦель игры= \n' \
                 'Бегай убивай: у тебя есть Бомба и Мина, но обудь осторожен, всего 1 жизнь \n' \
                 'P.S. Враги со временем становятся сильнее!'


def get_info_game(widget):
    """
    Метод вывод игровую справку.
    :return:
    """
    QMessageBox.question(widget, 'INFO Message',
                         MESSAGE_INFO_GAME,
                         QMessageBox.Yes, QMessageBox.No)


def get_iter(collection):
    """
    Метод получения Итераторо от переданной колекции.
    :param collection:
    :return:
    """
    return iter(collection)


MAPS = [os.path.join('map', 'map.txt'), os.path.join('map',  'map_2.txt'), os.path.join('map', 'map_3.txt')]
ITER_MAP = get_iter(MAPS)
next(ITER_MAP)


def method_load_player(load_list):
    """
    Метод заменяет глобальную переменную LIST_PLAYERS на параметр из загруженной игрый.
    :param load_list: Параметр считанный из сохранения.
    :return: None
    """
    global LIST_PLAYERS
    LIST_PLAYERS = load_list


def method_load_enemy(load_list):
    """
    Метод заменяет глобальную переменную LIST_ENEMY на параметр из загруженной игрый.
    :param load_list: Параметр считанный из сохранения.
    :return: None
    """
    global LIST_ENEMY
    LIST_ENEMY = load_list


def method_load_bomb(load_list):
    """
    Метод заменяет глобальную переменную SET_BOMBS на параметр из загруженной игрый.
    :param load_list: Параметр считанный из сохранения.
    :return: None
    """
    global SET_BOMBS
    SET_BOMBS = load_list


def method_load_bonus(load_list):
    """
    Метод заменяет глобальную переменную SET_BONUS на параметр из загруженной игрый.
    :param load_list: Параметр считанный из сохранения.
    :return: None
    """
    global SET_BONUS
    SET_BONUS = load_list
