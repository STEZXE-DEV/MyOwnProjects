# klasa wszystkich bytów
class Entity:
    def __init__(self, x, y, max_hp):
        self.x = float(x)
        self.y = float(y)
        self.max_hp = max_hp
        self.hp = max_hp
        self.lvl = 1
        self.entity_type = "Entity"
        self.power = 0

    # funkcja sprawdzająca czy byt żyje
    def is_alive(self):
        return self.hp > 0
    
    # funkcja poruszania się bytu
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    # otrzymywanie obrażeń
    def take_damage(self, dmg):
        if dmg >= self.hp:
            self.hp = 0
        else:
            self.hp = self.hp - dmg
         
    # leczenie się
    def heal(self, amount):
        if amount + self.hp <= self.max_hp:
            self.hp = self.hp + amount
        else:
            self.hp = self.max_hp

    # funkcja do późniejszego sprawdzania kolizji np. z jakimś elementem mapy
    def collision_with(self, dx, dy):
        return False



# # --- Testowy obiekt ---
# entity = Entity(10, 20, 100)

# print("=== START ===")
# print(f"Pozycja startowa: ({entity.x}, {entity.y})")
# print(f"HP startowe: {entity.hp}/{entity.max_hp}")
# print(f"Czy żyje? {entity.is_alive()}")
# print(f"Poziom: {entity.lvl}")

# # --- Test ruchu ---
# entity.move(5, -3)
# print("\n=== TEST RUCHU ===")
# print(f"Nowa pozycja: ({entity.x}, {entity.y})")  # powinno być (15, 17)

# # --- Test obrażeń ---
# entity.take_damage(30)
# print("\n=== TEST OTRZYMYWANIA OBRAŻEŃ ===")
# print(f"HP po 30 dmg: {entity.hp}")  # powinno być 70
# print(f"Czy żyje? {entity.is_alive()}")  # True

# entity.take_damage(100)
# print(f"HP po 100 dmg: {entity.hp}")  # powinno być 0
# print(f"Czy żyje? {entity.is_alive()}")  # False

# # --- Test leczenia ---
# entity.heal(50)
# print("\n=== TEST LECZENIA ===")
# print(f"HP po leczeniu 50: {entity.hp}")  # powinno być 50

# entity.heal(100)
# print(f"HP po leczeniu 100: {entity.hp}")  # powinno być max_hp = 100

# --- Test ponownego otrzymania obrażeń ---
# entity.take_damage(1000)
# print("\n=== TEST ŚMIERCI ===")
# print(f"HP po dmg: {entity.hp}")  # 0
# print(f"Czy żyje? {entity.is_alive()}")  # False
