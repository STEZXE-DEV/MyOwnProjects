from .entity import Entity
import random as r

# klasa obiektu przeciwnika
class Enemy(Entity):
    def __init__(self, x: int, y: int, level: int = None, max_hp: int = None, power: int = None) -> None:

        """
        Docstring for __init__
        
        :param x: pozycja przeciwnika w osi x
        :param y: pozycja przeciwnika w osi y 
        :param level: poziom doświadczenia przeciwnika
        :param max_hp: ilość maksymalnych punktów zdrowia przeciwnika
        :param hp: aktualna ilość punktów zdrowia przeciwnika
        :param power: moc przeciwnika, która wpływa na zadawane obrażenia
        :param entity_type: rodzaj bytu, w tym przypadku Enemy

        """

        if level is None:
            level = r.randint(1, 10)
        if power is None:
            power = r.randint(level * 10, level * 20 + 1)
        if max_hp is None:
            max_hp = level * 100

        super().__init__(x, y, max_hp)
        self.power = power
        self.level = level
        self.entity_type = "Enemy"

    # zwraca bazowe obrażenia zadawane przez przeciwnika
    def enemy_base_damage(self) -> int:
        return self.level ** 2 * self.power
    
    # oblicza maksymalne zdrowie przeciwnika i wypełnia zdrowie do wartości maksymalnej
    def calculate_max_hp(self) -> None:
        self.max_hp = self.level ** 2 * 10
        self.hp = self.max_hp

