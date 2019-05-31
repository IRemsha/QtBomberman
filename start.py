#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import map
from constants import MESSAGE_ERROR_LOAD_GAME, MESSAGE_INFO_GAME
from constants import HEIGHT_MAP, WIDTH_MAP, LIST_PLAYERS, LIST_ENEMY
import GUI
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QDesktopWidget, QComboBox, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt
from player import Player
from enemy import fill_list_enemy


class Menu(QWidget):
    """
    Класс реализует объект игрового окно меню со всеми его свйоствами и методами.
    """

    def __init__(self):
        super().__init__()

        self.init_menu()
        self.screen = None

        self.resize(400, 250)
        self.center_menu()
        self.setWindowTitle('Menu')
        self.show()
        self.difficulty = 0.5
        self.animation = True

    def init_menu(self):
        """
        Метод инициализации окна.
        :return: None
        """
        self.init_buttons()
        self.init_labels()
        self.init_combo()

    def init_buttons(self):
        """
        Метод инициализации кнопок.
        :return: None
        """
        load_game_btn = QPushButton('Play', self)
        load_game_btn.resize(load_game_btn.sizeHint())
        load_game_btn.move(200, 100)
        load_game_btn.clicked.connect(self.run_game)

        setting_game_btn = QPushButton('Load', self)
        setting_game_btn.resize(setting_game_btn.sizeHint())
        setting_game_btn.move(100, 100)
        setting_game_btn.clicked.connect(self.load_game)

        get_info_btn = QPushButton('Info', self)
        get_info_btn.resize(setting_game_btn.sizeHint())
        get_info_btn.move(300, 100)
        get_info_btn.clicked.connect(self.info_game)

    def init_labels(self):
        """
        Метод инициализации лайблов.
        :return: None
        """
        label_player = QLabel("Difficulty", self)
        label_player.move(10, 85)
        label_player.adjustSize()

        label_comp = QLabel("Information", self)
        label_comp.move(300, 85)
        label_comp.adjustSize()

        label_play = QLabel("Play Game", self)
        label_play.move(200, 85)
        label_play.adjustSize()

        label_setting = QLabel("Load Game", self)
        label_setting.move(100, 85)
        label_setting.adjustSize()

        label_setting = QLabel("Animation", self)
        label_setting.move(10, 135)
        label_setting.adjustSize()

    def init_combo(self):
        """
        Метод инициализации шторок.
        :return: None
        """
        combo_player = QComboBox(self)
        combo_player.addItems(["Normal", "Easy", "Hard"])
        combo_player.activated[str].connect(self.on_activated_player_difficulty)
        combo_player.move(10, 100)

        combo_player = QComboBox(self)
        combo_player.addItems(["Animation", "No Animation"])
        combo_player.activated[str].connect(self.on_activated_player_animation)
        combo_player.move(10, 150)

    def run_game(self):
        """
        Метод создаёт монстров и добавляет их в множество врагов.
        Загружает основное игровое окно.
        :return: None
        """

        self.screen = GUI.Screen(self.difficulty, self.animation)
        self.screen.show()
        self.close()

    def load_game(self):
        try:
            map.load_map()
            self.run_game()
        except FileNotFoundError:
            button_reply = QMessageBox.question(self, 'Yps..',
                                                MESSAGE_ERROR_LOAD_GAME,
                                                QMessageBox.Yes, QMessageBox.No)
            if button_reply == QMessageBox.Yes:
                self.run_game()
            else:
                pass

    def info_game(self):
        """
        Метод вывод игровую справку
        :return:
        """
        QMessageBox.question(self, 'INFO Message',
                             MESSAGE_INFO_GAME,
                             QMessageBox.Yes, QMessageBox.No)

    def on_activated_player_difficulty(self, text):
        """
        Метод отклик на действия игрока в шторке.
        (но пока-что я не перенёс функционал в это окно и оно выдаёт ошибку, при попытки изменить параметр)
        :return: None
        """
        if text == "Easy":
            self.difficulty = 0.8
        elif text == "Normal":
            self.difficulty = 0.5
        elif text == "Hard":
            self.difficulty = 0.1

        else:
            print("Выберете сложность")

    def on_activated_player_animation(self, text):
        """
        Метод отклик на действия игрока в шторке.
        (но пока-что я не перенёс функционал в это окно и оно выдаёт ошибку, при попытки изменить параметр)
        :return: None
        """
        if text == "Animation":
            self.animation = True
        elif text == "No Animation":
            self.animation = False
        else:
            print("Выберете анимацию")

    def center_menu(self):
        """
        Метод размещает игровое окно по середине экрана.
        :return: None
        """
        geometry_menu = self.frameGeometry()
        center_menu = QDesktopWidget().availableGeometry().center()
        geometry_menu.moveCenter(center_menu)
        self.move(geometry_menu.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = Menu()
    sys.exit(app.exec_())
