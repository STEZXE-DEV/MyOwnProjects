from entity import Entity

# funkcja licząca wartość n-elementu ciągu
def fibonacci(n):
    if n <= 0:
        return 0
    else:
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

# klasa postaci/gracza
class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, max_hp=100)
        self.exp = 0
        self.entity_type = "Player"

        # statystyki domyślne gracza
        self.power = 0 # potęga - zwiększa zadawane obrażenia przeciwnikowi
        self.focus = 0 # skupienie - wydłuża czas na wykoanie zadania
        self.conclusion = 0 # wniosek - zmniejsza otrzymywane obrażenia od wrogów
        self.unassigned_stat_points = 0 # każdy poziom daje wolne punkty do rozdania
    
    def max_exp_per_lvl(self):
        return fibonacci(self.lvl + 1) * 20 # wzór na maksymalną ilość EXP dla poszczególnego poziomu
    
    def amount_of_unassigned_stat_points(self):
        return int(self.lvl * 2) # wzór na punkty do przydzielenia

    def level_up(self, amount):
        self.exp += amount
        while self.exp >= self.max_exp_per_lvl(): #kiedy osiągany jest limit lub limit jest przekroczony
            self.exp -= self.max_exp_per_lvl()
            self.lvl += 1
            self.unassigned_stat_points += self.amount_of_unassigned_stat_points()
            self.hp += self.lvl * 10 # zwiększenie HP (pozwala na uzyskanie HP nie będąc w pełni uleczonym)
            self.max_hp += self.lvl * 10 # zwiększenie MAX_HP o tą samą wartość co HP

    def assign_stat_points(self, stat, amount=1): #domyślnie ilość 1
        if 0 < amount <= self.unassigned_stat_points: #ilość punktów jakie chcemy przydzielić musi być mniejsza/równa ilości nieprzypisanych punktów które mamy
            if stat == "POWER":
                self.power += amount
            elif stat == "FOCUS":
                self.focus += amount
            elif stat == "CONCLUSION":
                self.conclusion += amount
            self.unassigned_stat_points -= amount
        else: raise ValueError("You don't have enough points to assign")


player = Player(0,0)
