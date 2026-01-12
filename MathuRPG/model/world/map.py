from .tile import Tile

# klasa mapy w grze
class Map:
    def __init__(self, width: int, height: int, default_tile) -> None:

        """
        Docstring for __init__
        
        :param width: szerokość mapy
        :param height: wysokość mapy
        :param default_tile: domyślny kafelek budujący mapę

        """ 

        self.width = width
        self.height = height
        self.default_tile = default_tile
        self.grid = self.grid = [[Tile(default_tile.tile_type, default_tile.walkable) for _ in range(width)] for _ in range(height)] # dwuwymiarowa plansza złożona z kafelków

    # sprawdza czy obie współrzędne mieszczą się w granicach mapy
    def in_map_bounds(self, x: int, y: int) -> bool:

        """
        Docstring for in_map_bounds
        
        :param x: położenie obiektu w osi x
        :param y: położenie obiektu w osi y

        """

        return 0 <= x < self.width and 0 <= y < self.height
    
    # zwraca konkretny kafelek
    def get_tile(self, x: int, y: int):

        """
        Docstring for get_tile

        :param x: położenie żądanego kafelka w osi x
        :param y: położenie żądanego kafelka w osi y

        """

        if not self.in_map_bounds(x, y):
            return None
        return self.grid[y][x]
    
    # ustawia konkretny kafelek
    def set_tile(self, x: int, y: int, tile):

        """
        Docstring for set_tile
        
        :param x: położenie kafelka, którego chcemy ustawić w osi x
        :param y: położenie kafelka, którego chcemy ustawić w osi x
        :param tile: obiekt kafelka

        """

        if self.in_map_bounds(x, y):
            self.grid[y][x] = tile

    # funkcja dla bytu do sprawdzenia możliwości przejścia na następny kafelek 
    def try_move(self, entity, dx: int, dy: int) -> None:
        
        """

        Docstring for try_move
        
        :param entity: callback do entity
        :param dx: przesunięcie bytu w osi x
        :param dy: przesunięcie bytu w osi y

        """

        new_x = entity.x + dx
        new_y = entity.y + dy

        # kafelek musi być w granicach mapy
        if not self.in_map_bounds(new_x, new_y):
            return None
            
        new_tile = self.get_tile(new_x, new_y)

        # kafelek musi być przechodni
        if not new_tile.is_walkable():
            return None
        
        if new_tile.get_entity():
            return new_tile.get_entity()
        
        old_tile = self.get_tile(entity.x, entity.y)
        if old_tile:
            old_tile.action_on_exit(entity) # byt schodzi ze starego kafelka i wykonuje się akcja z tym związana
            old_tile.set_entity(None) # na starym kafelku nie ma już żadnego bytu
        entity.move(dx, dy) # byt przechodzi na nowy kafelek
        new_tile.set_entity(entity) # byt jest na nowym kafelku
        new_tile.action_on_enter(entity) # działanie po wejściu bytu na kafelek
            
    # funkcja do sprawdzania kolizji z inny bytem na kafelku
    def collision_with_entity(self, entering_entity) -> str:

        """
        Docstring for collision_with_entity
        

        :param entity: byt, który dociera właśnie na kafelek

        """

        current_tile = self.get_tile(entering_entity.x, entering_entity.y)

        entity = current_tile.get_entity()
        
        if entity:
            return entity.entity_type # czy na obecnym kafelku jest byt (zwraca rodzaj bytu jeśli jakiś jest)
        
        
    def is_collision_player_with_enemy(self, entering_entity) -> bool:

        """
        Docstring for is_collision_player_with_enemy
        
        :param entering_entity: byt, który wchodzi na kafelek

        """

        player_steps_on_enemy = entering_entity.entity_type == "Player" and self.collision_with_entity(entering_entity) == "Enemy"
        enemy_steps_on_player = entering_entity.entity_type == "Enemy" and self.collision_with_entity(entering_entity) == "Player"

        return player_steps_on_enemy or enemy_steps_on_player
