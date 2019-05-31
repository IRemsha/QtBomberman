import unittest
import map

from bomb import SimpleBomb, Mine
from bonus import Bonus
from constants import SET_BOMBS, LIST_PLAYERS, SET_BONUS, LIST_ENEMY, SET_EXPLOSIONS
from enemy import Lower
from explosion import Explosion
from player import Player


class BombTest(unittest.TestCase):
    def setUp(self):
        self.player = Player([1, 1])

    def test_two_bomb_boom(self):

        green_bomb_one = Mine(self.player.position, self.player, self.player.power_bomb)
        green_bomb_two = Mine(self.player.position, self.player, self.player.power_bomb)

        SET_BOMBS.add(green_bomb_one)
        SET_BOMBS.add(green_bomb_two)

        green_bomb_one.boom()

        self.assertEqual(green_bomb_two, SET_BOMBS.pop())

    def test_bomb_tick(self):
        simple_bomb = SimpleBomb(self.player.position, self.player, self.player.power_bomb)

        SET_BOMBS.add(simple_bomb)

        for i in range(11):
            simple_bomb.ticker()

        self.assertEqual(0, SET_BOMBS.__len__())


class BonusTest(unittest.TestCase):
    def setUp(self):
        self.player = Player([1, 1])
        LIST_PLAYERS.append(self.player)

    def test_bonus_up(self):
        current_count_bomb = self.player.count_bomb
        bonus = Bonus(self.player.position)
        bonus.up_player()

        self.assertEqual(current_count_bomb+0.5, self.player.count_bomb)

    def test_bonus_up_portal(self):
        bonus_d = Bonus(self.player.position, True)
        bonus_d.up_player()
        self.assertEqual(4, LIST_ENEMY.__len__())


class ExplosionTest(unittest.TestCase):
    def setUp(self):
        self.player = Player([1, 1])
        LIST_PLAYERS.append(self.player)

    def test_explosion_tick(self):
        simple_bomb = SimpleBomb(self.player.position, self.player, self.player.power_bomb)
        explosion = Explosion(simple_bomb.position, simple_bomb, simple_bomb.power_bomb)

        SET_EXPLOSIONS.clear() # почему он уже не пустой?
        SET_EXPLOSIONS.add(explosion)

        for i in range(2):
            explosion.ticker()

        self.assertEqual(0, SET_EXPLOSIONS.__len__())


class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.player = Player([10, 10])
        LIST_PLAYERS.append(self.player)
        self.simple_bomb = SimpleBomb(self.player.position, self.player, self.player.power_bomb)
        self.green_bomb = Mine(self.player.position, self.player, self.player.power_bomb)

    def test_refresh_bomb(self):
        # Бесполезный
        current_bomb = self.player.count_bomb
        self.player.refresh_bomb()
        self.assertEqual(current_bomb+1, self.player.count_bomb)

    def test_roll_bomb1(self):
        self.player.type_bomb = 0
        self.player.roll_bomb()

        self.assertEqual(1, self.player.type_bomb)

    def test_roll_bomb2(self):
        self.player.type_bomb = 1
        self.player.roll_bomb()

        self.assertEqual(0, self.player.type_bomb)

    def test_drop_bomb_simple(self):
        self.player.type_bomb = 0

        map.set_object(self.player.position, self.player)
        self.player.drop_bomb()
        print(SET_BOMBS.__len__())

        self.assertEqual(type(self.simple_bomb), type(SET_BOMBS.pop()))

    def test_drop_bomb_green(self):
        self.player.type_bomb = 1

        map.set_object(self.player.position, self.player)
        self.player.drop_bomb()
        print(SET_BOMBS.__len__())

        self.assertEqual(type(self.green_bomb), type(SET_BOMBS.pop()))

    def test_drop_bomb_empty(self):
        self.player.type_bomb = 1
        self.player.count_bomb = 0

        map.set_object(self.player.position, self.player)
        self.player.drop_bomb()
        print(SET_BOMBS.__len__())

        self.assertEqual(0, SET_BOMBS.__len__())

    def test_move_left(self):
        map.read_map('map\map.txt')
        direction = 'left'
        map.set_object(self.player.position, self.player)

        maybe_new_position = list(self.player.position)
        maybe_new_position[0] -= self.player.step

        self.player.move(direction)

        self.assertEqual(map.get_object(maybe_new_position), map.get_object(self.player.position))

    def test_move_right(self):
        map.read_map('map\map.txt')
        direction = 'right'
        map.set_object(self.player.position, self.player)

        maybe_new_position = list(self.player.position)
        maybe_new_position[0] += self.player.step

        self.player.move(direction)

        self.assertEqual(map.get_object(maybe_new_position), map.get_object(self.player.position))

    def test_move_up(self):
        map.read_map('map\map.txt')
        direction = 'up'
        map.set_object(self.player.position, self.player)

        maybe_new_position = list(self.player.position)
        maybe_new_position[1] -= self.player.step

        self.player.move(direction)

        self.assertEqual(map.get_object(maybe_new_position), map.get_object(self.player.position))

    def test_move_down(self):
        map.read_map('map\map.txt')
        direction = 'down'
        map.set_object(self.player.position, self.player)

        maybe_new_position = list(self.player.position)
        maybe_new_position[1] += self.player.step

        self.player.move(direction)

        self.assertEqual(map.get_object(maybe_new_position), map.get_object(self.player.position))

    def test_give_dmg(self):
        current_hit = self.player.hit_point
        dmg = 3
        self.player.give_damage(dmg)
        self.assertEqual(current_hit-3, self.player.hit_point)

    def test_player_dead(self):
        current_position = self.player.position
        self.player.death()
        self.assertEqual(None, map.get_object(current_position))


class MapTest(unittest.TestCase):

    def setUp(self):
        self.player = Player([10, 10])
        self.simple_bomb = SimpleBomb(self.player.position, self.player, self.player.power_bomb)

    def test_move_wall(self):
        map.read_map('map\map.txt')
        direction = 'left'
        self.player.position = [1, 1]
        map.set_object(self.player.position, self.player)

        default_position = self.player.position

        maybe_new_position = list(self.player.position)
        maybe_new_position[0] -= self.player.step

        self.player.move(direction)

        self.assertEqual(map.get_object(default_position), map.get_object(self.player.position))

    def test_move_bomb(self):
        map.read_map('map\map.txt')
        direction = 'right'
        self.player.position = [1, 1]
        self.simple_bomb.position = [2, 1]
        map.set_object(self.player.position, self.player)
        map.set_object(self.simple_bomb.position, self.simple_bomb)

        default_position = self.player.position

        maybe_new_position = list(self.player.position)
        maybe_new_position[0] += self.player.step

        self.player.move(direction)

        self.assertEqual(map.get_object(default_position), map.get_object(self.player.position))

    def test_move_enemy(self):
        map.read_map('map\map.txt')
        direction = 'right'
        self.player.position = [1, 1]
        enemy = Lower([2, 1])
        map.set_object(self.player.position, self.player)
        map.set_object(enemy.position, enemy)

        default_position = self.player.position

        maybe_new_position = list(self.player.position)
        maybe_new_position[0] += self.player.step

        self.player.move(direction)

        self.assertEqual(map.get_object(default_position), map.get_object(self.player.position))

    def test_move_bonus(self):
        map.read_map('map\map.txt')
        direction = 'right'
        self.player.position = [1, 1]
        bonus = Bonus([2, 1])
        map.set_object(self.player.position, self.player)
        map.set_object(bonus.position, bonus)

        maybe_new_position = list(self.player.position)
        maybe_new_position[0] += self.player.step

        self.player.move(direction)

        self.assertEqual(map.get_object(maybe_new_position), map.get_object(self.player.position))


if __name__ == '__main__':
    unittest.main()
