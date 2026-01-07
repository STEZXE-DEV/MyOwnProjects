# klasa wszystkich bytów
class Entity:
    def __init__(self, x: int, y: int, max_hp: int) -> None:

        """
        Docstring for __init__
        
        :param x: pozycja bytu w osi x
        :param y: pozycja bytu w osi y
        :param max_hp: maksymalne zdrowie bytu
        :param hp: aktualne zdrowie bytu
        :param lvl: poziom doświadczenia bytu
        :param entity_type: rodzaj bytu np. Player
        :param power: moc bytu, która zwiększa zadawane przez byt obrażenia

        """

        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.hp = max_hp
        self.lvl = 1
        self.entity_type = "Entity"
        self.power = 0
        self.alive = True


    # funkcja sprawdzająca czy byt żyje
    def is_entity_alive(self) -> bool:
        return self.hp > 0
    
    # funkcja poruszania się bytu
    def move(self, dx: int, dy: int) -> None:
        
        """
        Docstring for move
        
        :param dx: wartość przesunięcia bytu w osi x
        :param dy: wartość przesunięcia bytu w osi y

        """

        self.x += dx
        self.y += dy

    # otrzymywanie obrażeń
    def take_damage(self, dmg: int) -> None:

        """
        Docstring for take_damage
        
        :param dmg: ilość podstawowych obrażeń które zostaną zadane bytowi

        """
        if dmg <= 0:
            dmg = 1

        if dmg >= self.get_hp():
            self.hp = 0
            self.alive = False
        else:
            self.hp = self.hp - dmg
         
    # leczenie się (uzupełnienie zdrowia nigdy nie przekroczy maksymalnego zdrowia bytu)
    def heal(self, amount: int) -> None:

        """
        Docstring for heal
        
        :param amount: ilość punktów zdrowia, które zostanie odzyskane

        """

        if amount + self.hp <= self.max_hp:
            self.hp = self.hp + amount
        else:
            self.hp = self.max_hp

    # getter życia bytu
    def get_hp(self) -> int:
        return self.hp
