import os
from pathlib import Path

import map
from constants import (SET_TYPE_BLOCK, SET_BOMBS, SET_EXPLOSIONS, LIST_ENEMY, HEIGHT_MAP, WIDTH_MAP, SIZE_PIXEL_BLOCK,
                       SET_BONUS, COLOR_BLACK, get_info_game)
import constants
from PyQt5.QtGui import QIcon, QPainter, QBrush, QColor, QFont, QPixmap, QMovie
from PyQt5.QtCore import Qt, QBasicTimer, QPropertyAnimation, QRect, QPointF
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QDesktopWidget, QComboBox, QLabel, QMessageBox,
                             QMainWindow, QHBoxLayout, QFrame)
from bomb import SimpleBomb
from enemy import fill_list_enemy
from player import Player

block_images = [QColor(8, 122, 46), QColor(255, 197, 63), QColor(133, 131, 133)]


def update_bonus():
    """
    Метод update для SET_BONUS.
    :return: None
    """
    for bonus in constants.SET_BONUS.copy():
        map.set_object(bonus.position, bonus)
        # костыль от загрузки одного объекта с разным хешем, типа протыкиваю по каждому бонусу


def update_bomb():
    """
    Метод update для SET_BOMBS.
    :return: None
    """
    for bomb in constants.SET_BOMBS.copy():  # узнать что происходит
        if bomb.assets:
            bomb.ticker()


def update_explosion():
    """
    Метод update для SET_EXPLOSIONS.
    :return: None
    """
    for explosion in constants.SET_EXPLOSIONS.copy():
        explosion.ticker()


def update_player(player):
    """
    Метод update для PLAYER.
    :return: None
    """
    if player.hit_point < 1:
        player.death()
        return True


def update_enemy():
    """
    Метод update для LIST_ENEMY.
    :return: None
    """
    for enemy in constants.LIST_ENEMY.copy():
        enemy.choose_direction()
        if enemy.hit_point < 1:
            enemy.death()


def get_rect(position):
    """
    Метод возвращающий ТЕЛО квадрата по координатам его леврнр верхнего угла.
    :param position: Параметр координат квадрата.
    :return: Rect
    """
    rect = position[0] * SIZE_PIXEL_BLOCK, position[1] * SIZE_PIXEL_BLOCK, SIZE_PIXEL_BLOCK, SIZE_PIXEL_BLOCK
    return rect


class Screen(QMainWindow):
    """
    Класс реализуе объект главного игрового экрана со всеми его свйоствами и методами.
    """
    def __init__(self, conf, animation):
        super().__init__()

        self.animation = animation
        self.screen_for_animation = None
        self.init_screen()
        self.player = Player([1, 1], coef_speed_enemy=conf, screen=self.screen_for_animation)
        constants.LIST_PLAYERS.append(self.player)
        self.timer = QBasicTimer()
        self.step = 0
        self.step2 = 5
        self.timer.start(100, self)
        self.qp = QPainter()
        self.anime_player = QLabel(self.screen_for_animation)

        if self.screen_for_animation:
            self.anime_player3(self.player.position, )
        fill_list_enemy(self.screen_for_animation)
        self.show()

    def init_screen(self):
        """
        Метод инициализации окна.
        :return: None
        """
        self.resize(WIDTH_MAP, HEIGHT_MAP)
        self.center_screen()
        self.setWindowTitle('Screen game')
        if self.animation:
            self.screen_for_animation = self

        self.show()

    def paintEvent(self, event):
        """
        Метод отрисовки событий.По событию отрисовывает объекты на карте и текст.
        :param event: Параметр события.
        :return: None
        """
        self.qp.begin(self)
        self.draw_stuff()
        self.draw_text(event)
        self.qp.end()

    def draw_stuff(self):
        """
        Метод вызывающий поэлементную отрисовку объектов игры.
        :return: None
        """
        self.draw_map()
        if self.animation:
            self.draw_enemy_anim()
            self.draw_bombs_anim()
            self.draw_explosions_anim()

        else:
            self.draw_player()
            self.draw_enemy_no_anim()
            self.draw_bombs_no_anim()
            self.draw_explosions_no_anim()

        self.draw_bonus()

    def draw_text(self, event):
        """
        Метод рисующий красивый тест.
        :param event: Параметр события.
        :return: None
        """
        # self.qp.setPen(QColor(168, 34, 3))
        # self.qp.setFont(QFont('Decorative', 8))
        # self.qp.drawText(*get_rect((0, 0)), Qt.AlignCenter, '~(;_._;)~')

        pass

    def keyPressEvent(self, event):
        """
        Метод обработки ввода с клав.
        :param event: Параметр сигнала с квал.
        :return: None
        """
        if event.key() == Qt.Key_Left:
            self.player.move('left')
            self.player.anim_left = True
        elif event.key() == Qt.Key_Right:
            self.player.move('right')
            self.player.anim_right = True
        elif event.key() == Qt.Key_Up:
            self.player.move('up')
            self.player.anim_up = True
        elif event.key() == Qt.Key_Down:
            self.player.move('down')
            self.player.anim_down = True

        elif event.key() == Qt.Key_Shift:
            self.player.roll_bomb()
        elif event.key() == Qt.Key_Space:
            self.player.drop_bomb()

        elif event.key() == Qt.Key_S:
            map.save_map()

        elif event.key() == Qt.Key_L:
            map.load_map()
        elif event.key() == Qt.Key_I:
            get_info_game(self)
        elif event.key() == Qt.Key_N:
            map.scroll_map()

        self.update()

    def timerEvent(self, event):
        """
        Метод Апдейтов(?) и вывод тулбара для игрока.
        :param event: Параметр события.
        :return: None
        """
        update_bomb()
        update_explosion()
        update_bonus()
        self.player = constants.LIST_PLAYERS[0] # КОСТЫЛЬ НА СОХРАНЕНИЯ ПОЗИЦИИ ИГРОКА ПРИ ЗАГРУЗКЕ
        if self.step2/10 > self.player.coef_speed_enemy: # temp
            update_enemy()
            self.step2 = 0 # temp

        self.statusBar().showMessage('Время: {} | Жизни: {} | Бомбы: {} | Тип: {} | Монстров на карте: {} | {}'.format(
                                                                                    self.step/10,
                                                                                    self.player.hit_point,
                                                                                    self.player.count_bomb,
                                                                                    'Обычные',
                                                                                    len(LIST_ENEMY),
                                                                                    self.player.type_bomb))

        if update_player(self.player):
            reply = QMessageBox.question(self, 'Repeat?', "\tGAME OVER \nЗагрузить последнее сохранение?",
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                map.load_map()
            else:
                print('КОНЕЦ ИГРЫ')
                self.close()

        self.step += 1
        self.step2 += 1

    def center_screen(self):
        """
        Метод размещает игровое окно по середине экрана.
        :return: None
        """
        geometry_screen = self.frameGeometry()
        center_screen = QDesktopWidget().availableGeometry().center()
        geometry_screen.moveCenter(center_screen)
        self.move(geometry_screen.topLeft())

    def anime_player3(self, start, end=None):
        if end is None:
            end = [1, 1]
        movie = QMovie(os.path.join('gif', 'player.gif'))
        self.anime_player.setMovie(movie)
        movie.start()
        self.anime_player.show()

        self.anim = QPropertyAnimation(self.anime_player, b'pos')
        self.anim.setDuration(200)
        self.anim.setStartValue(QPointF(start[0]*50, start[1]*50))
        self.anim.setEndValue(QPointF(end[0]*50, end[1]*50))
        self.anim.start()

    def draw_player(self):
        """
        Метод рисует Players.
        :return: None
        """
        rect = get_rect(self.player.position)

        self.qp.setBrush(self.player.color)
        self.qp.drawRect(rect[0]+5, rect[1]+5, rect[2]-10, rect[3]-10)

        self.update()

    def draw_enemy_anim(self):
        """
        Метод рисует LIST_ENEMY.
        :return: None
        """
        for enemy in constants.LIST_ENEMY.copy():
            rect = get_rect(enemy.position)
            enemy.anime_enemy.setMovie(enemy.movie)
            enemy.anime_enemy.setGeometry(*rect)

            enemy.anime_enemy.show()

    def draw_enemy_no_anim(self):
        """
        Метод рисует LIST_ENEMY.
        :return: None
        """
        for enemy in constants.LIST_ENEMY.copy():
            rect = get_rect(enemy.position)
            self.qp.setBrush(enemy.color)
            self.qp.drawRect(rect[0] + 5, rect[1] + 5, rect[2] - 10, rect[3] - 10)

    def draw_map(self):
        """
        Метод рисует Map.
        :return: None
        """
        for x in range(13):
            for y in range(13):
                self.draw_block(map.visible_game_map[x][y], [x, y])

    def draw_block(self, current_block, position):
        """
        Метод рисует Block.
        :return: None
        """
        if current_block.block_type == 0:

            return
        img = block_images[current_block.block_type]
        rect = get_rect(position)
        self.qp.setBrush(img)
        self.qp.drawRect(*rect)

        if current_block.block_type == 2:
            self.draw_texture_block(position)

    def draw_texture_block(self, position):
        """
        Метод рисует Block.
        :return: None
        """
        rect = get_rect(position)
        self.qp.setBrush(Qt.BDiagPattern)
        self.qp.drawRect(*rect)

    def draw_bombs_anim(self):
        """
        Метод рисует SET_BOMBS.
        :return: None
        """

        for bomb in constants.SET_BOMBS.copy().copy():
            rect = get_rect(bomb.position)

            bomb.anime_bomb.setMovie(bomb.movie)
            bomb.anime_bomb.setGeometry(*rect)
            bomb.anime_bomb.show()
        self.update()

    def draw_bombs_no_anim(self):
        """
        Метод рисует SET_BOMBS.
        :return: None
        """

        for bomb in constants.SET_BOMBS.copy().copy():
            rect = get_rect(bomb.position)
            if bomb.anim & bomb.assets:
                self.qp.setBrush(QColor(128, 0, 0))
                self.qp.drawEllipse(rect[0] + 10, rect[1] + 10, rect[2] - 20, rect[3] - 20)
                bomb.anim = False
            else:
                self.qp.setBrush(bomb.color)
                bomb.anim = True
                self.qp.drawEllipse(rect[0] + 5, rect[1] + 5, rect[2] - 10, rect[3] - 10)

        self.update()

    def draw_explosions_anim(self):
        """
        Метод рисует SET_EXPLOSIONS.
        :return: None
        """
        for explosion in constants.SET_EXPLOSIONS.copy():
            rect = get_rect(explosion.position)
            explosion.anime_expl.setMovie(explosion.movie)
            explosion.anime_expl.setGeometry(*rect)
            explosion.anime_expl.show()

    def draw_explosions_no_anim(self):
        """
        Метод рисует SET_EXPLOSIONS.
        :return: None
        """
        for explosion in constants.SET_EXPLOSIONS.copy():
            rect = get_rect(explosion.position)
            self.qp.setBrush(QColor(255, 241, 49))
            self.qp.drawEllipse(*rect)
            self.draw_texture_explosions(explosion)

    def draw_texture_explosions(self, explosion):
        """
        Метод рисует SET_EXPLOSIONS.
        :return: None
        """
        rect = get_rect(explosion.position)
        self.qp.setBrush(Qt.Dense2Pattern)
        self.qp.drawEllipse(*rect)

        self.update()

    def draw_bonus(self):
        """
        Метод рисует SET_BONUS.
        :return: None
        """
        for bonus in constants.SET_BONUS.copy():
            rect = get_rect(bonus.position)
            self.qp.setBrush(bonus.color)
            self.qp.drawEllipse(rect[0]+10, rect[1]+10, rect[2]-20, rect[3]-20)

