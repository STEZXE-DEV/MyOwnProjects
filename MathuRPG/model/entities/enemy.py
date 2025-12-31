from entity import Entity
# from player import Player
import random as r

class Enemy(Entity):
    def __init__(self, x, y, level=1, power=1):
        super().__init__(x, y, max_hp=1)
        self.hp = self.max_hp
        self.max_hp = self.max_hp
        self.power = int(power)
        self.lvl = int(level)
        self.entity_type = "Enemy"

    def enemy_base_damage(self):
        return self.lvl ** 2 * self.power
    
    def randomized_enemy_stats(self):
        self.lvl = r.randint(1, 10)
        self.power = r.randint(self.lvl ** 2, self.lvl * 100)
    
    def calculate_max_hp(self):
        self.max_hp = self.lvl ** 2 * 10
        self.hp = self.max_hp


# player = Player(0, 0)
# player.unassigned_stat_points = 10
# player.assign_stat_points("CONCLUSION", 5)
# enemy = Enemy(0, 0)
# enemy.power = 25
# enemy.lvl = 2

# print("HP before:", player.hp)
# enemy.deal_damage_to_(player, enemy.calculate_damage_to_player(player))
# print("HP after:", player.hp)







