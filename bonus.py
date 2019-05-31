from PyQt5.QtGui import QColor

import constants
import map


class Bonus:
    """
      Класс реализующий объект Bonus. Содержит все методы и свойства описывающие Bonus.
    """
    def __init__(self, position, portal=False, color=QColor(181, 228, 181)):
        self.position = position
        self.portal = portal
        self.color = color

    def up_player(self):
        """
        Метод - увеличение параметров игрока и вызов delete.
        :return: None
        """
        constants.LIST_PLAYERS[0].get_bonus()
        # написать лучше
        self.delete()

        if self.portal:
            map.scroll_map()
            constants.LIST_PLAYERS[0].position = [1, 1]
            return False
        return True

    def delete(self):
        """
        Метод удаляет Bonus из множестве и Объектной карты.
        :return: None
        """
        map.set_object(self.position, None)
        constants.SET_BONUS.discard(self)
