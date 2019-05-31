import os
import pickle
from pathlib import Path

from bonus import Bonus
from constants import SET_TYPE_BLOCK, SET_EXPLOSIONS, LIST_PLAYERS, LIST_ENEMY, SET_BOMBS, ITER_MAP
import constants

from bomb import Bomb, SimpleBomb, Mine
from player import Player
from enemy import Enemy, fill_list_enemy

map_list_bock = {'': SET_TYPE_BLOCK[0], '-': SET_TYPE_BLOCK[1], 'w': SET_TYPE_BLOCK[2]}


class Block:
    """
      Класс реализующий объект Block. Содержит все свойства описывающие Block.
    """
    def __init__(self, block_type=SET_TYPE_BLOCK[0]):
        self.block_type = block_type

    def iw_way(self):
        return self.block_type == SET_TYPE_BLOCK[0]

    def is_walled(self):
        return self.block_type != SET_TYPE_BLOCK[1] and self.block_type != SET_TYPE_BLOCK[2]

    def is_destroyable(self):
        return not self.block_type == SET_TYPE_BLOCK[2]


def read_map(file_map):
    """
    Методов считывает карту из txt документа при первом запуке.
    Создаётся 2 вида карты: a) Визуальная (блоки, взрывы) б) Объектная (Игрок, монсты, бомбы и бонусы).
    :return: None
    """
    text_map = open(file_map)
    global visible_game_map
    visible_game_map = [[Block() for x in range(13)] for y in range(13)]  # Так создаётся двумерный массив
    for i in range(13):
        line_map = text_map.readline()
        for j in range(13):
            visible_game_map[j][i] = Block(map_list_bock.get(line_map[j], SET_TYPE_BLOCK[0]))  # Значение ключа и дефолт
    global object_game_map
    object_game_map = [[None for x in range(13)] for y in range(13)]
    text_map.close()


read_map_file = True

if read_map_file:
    read_map(os.path.join('map', 'map.txt'))


def scroll_map():
    """
    Метод перехода на следующую карту.
    Какой же красивый метод, except правда убогий, а так красиво.
    :return:
    """
    constants.LIST_PLAYERS[0].position = [1, 1]
    try:
        read_map(next(ITER_MAP))
        fill_list_enemy()
    except StopIteration:
        print('КОНЕЦ ИГРЫ')


def save_map():
    """
    Метод сохранение игру по нажатию кл. S.
    Сохраняю параметры игры в разные файлы в папку save, на каждый параметр свой файл, сохраняю их в байтах пользуюсь,
    модулем pickle.
    :return: None
    """
    try:
        with open(os.path.join('save', 'data.pickle_map_visible_obj'), 'wb') as f:
            pickle.dump(visible_game_map, f)

        try:
            with open(os.path.join('save', 'data.pickle_players'), 'wb') as f:
                pickle.dump(constants.LIST_PLAYERS, f)
        except Exception as e:
            print(e)

        try:
            with open(os.path.join('save', 'data.pickle_bomb'), 'wb') as f:
                pickle.dump(constants.SET_BOMBS, f)
        except Exception as e:
            print(e)

        with open(os.path.join('save', 'data.pickle_bonus'), 'wb') as f:
            pickle.dump(constants.SET_BONUS, f)
        try:
            with open(os.path.join('save', 'data.pickle_map_obj'), 'wb') as f:
                pickle.dump(object_game_map, f)

        except Exception as e:
            print(e)

        try:
            with open(os.path.join('save', 'data.pickle_enemy'), 'wb') as f:
                pickle.dump(constants.LIST_ENEMY, f)
        except Exception as e:
            print(e)

    except FileNotFoundError:
        os.mkdir("save")
        save_map()
        print('Папка с сохранениями была создана')

    print('Игра сохранена')


def load_map():
    """
    Метод считываю и загружаю сохранения игры с папки save. После загружки параметров изменяю текущие значения в
    constants на загаруженные. Пользуюсь модулем pickle.
    :return: None
    """
    try:
        with open(os.path.join('save', 'data.pickle_map_visible_obj'), 'rb') as f:
            global visible_game_map
            visible_game_map = pickle.load(f)

        with open(os.path.join('save', 'data.pickle_map_obj'), 'rb') as f:
            global object_game_map
            object_game_map = pickle.load(f)

        with open(os.path.join('save', 'data.pickle_players'), 'rb') as f:
            load_list_player = pickle.load(f)
            constants.method_load_player(load_list_player)

        with open(os.path.join('save', 'data.pickle_enemy'), 'rb') as f:
            load_list_enemy = pickle.load(f)
            constants.method_load_enemy(load_list_enemy)

        with open(os.path.join('save', 'data.pickle_bomb'), 'rb') as f:
            load_list_bomb = pickle.load(f)
            constants.method_load_bomb(load_list_bomb)

        with open(os.path.join('save', 'data.pickle_bonus'), 'rb') as f:
            load_list_bonus = pickle.load(f)
            constants.method_load_bonus(load_list_bonus)
        print('Игра загружена')

    except FileNotFoundError:
        print('Сохранения не найдены')


def can_move(position):
    """
    Методо принимает парамтр position и проверяет может ли объет сделать шаг в данную клетку.
    Возрвращает True или False.
    :param position: Параметр принимат координату клетки поля, на которую он хочет перейти.
    :return: Bool
    """
    if not get_visible(position).is_walled():
        return False

    elif isinstance(get_object(position), Mine):
        get_object(position).assets = True
        return True

    elif isinstance(get_object(position), Bomb):
        return False

    elif isinstance(get_object(position), Player):
        get_object(position).give_damage(3)
        return True

    elif isinstance(get_object(position), Bonus):
        return get_object(position).up_player()

    elif isinstance(get_object(position), Enemy):
        return False

    obj_on_position = get_object(position)
    return True


def get_object(position):
    """
    Метод возвращает объет который находится по кординатам параметра position на Объектной карте.
    :param position: Параметр принимает координаты объета на карте.
    :return: Obj
    """
    return object_game_map[position[0]][position[1]]


def get_visible(position):
    """
    Метод возвращает объет который находится по кординатам параметра position на Визуальной карте.
    :param position: Параметр принимает координаты объета на карте.
    :return: Obj
    """
    return visible_game_map[position[0]][position[1]]


def set_object(position, obj):
    """
    Метод заменяет объет на Объектной карте с позицией position на новый obj.
    :param position: Параметр принимает координаты карты.
    :param obj: Параметр принимает объект.
    :return: None
    """
    object_game_map[position[0]][position[1]] = obj


def set_visible(position, vsbl):
    """
     Метод заменяет объет на Визуальной карте с позицией position на новый vsbl.
    :param position: Параметр принимает координаты карты.
    :param vsbl: Параметр принимает визульный объект.
    :return:  None
    """
    visible_game_map[position[0]][position[1]] = vsbl


def can_drop(enemy):
    """
    Метод ставит Bonus на Объектную карту.
    :param enemy: Параметр врага, который оставил после смерти Bonus.
    :return: None.
    """
    set_object(enemy.position, Bonus(enemy.position))


def blow_up_block(position):
    """
    Метод разрушает блоки от взрыва. Заменяем блок стены на Визуальной карте, на блок пустоты.
    :param position: Параметр принимает координаты блока.
    :return: None
    """
    if isinstance(visible_game_map[position[0]][position[1]], Block):
        set_visible(position, Block())

    #   Костыли и заметки
    #   if isinstance(object_game_map[position[0]][position[1]], SimpleBomb):
    #   get_object(position).remove()
    #   В таком варианте бомба не уничтожает бомбу.


def damage_bomb(position, power):
    """
    Метод выполняет функцию нанести урон объетам, попавшим в радиус взрыва.
    :param position: Параметр принимает координату точки взрыва.
    :param power: Параметр принимает силу взрыва.
    :return: None
    """
    if isinstance(object_game_map[position[0]][position[1]], Player):
        get_object(position).give_damage(power)

    if isinstance(object_game_map[position[0]][position[1]], Enemy):
        get_object(position).give_damage(power)



