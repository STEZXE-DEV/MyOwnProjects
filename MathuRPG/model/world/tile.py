# klasa kafelka
class Tile:
    def __init__(self, tile_type: str, walkable: bool, entity_on=None, on_enter=None, on_exit=None) -> None:

        """
        Docstring for __init__
        
        :param tile_type: rodzaj kafelka np. trawa, ściana, skrzynia
        :param entity_on: byt aktualnie znajdujący się na kafelku - callback
        :param walkable: czy można po kafelku się poruszać (stać na nim)
        :param on_enter: działanie względem bytu po wejściu na kafelek
        :param on_exit: działanie względem bytu po zejściu z kafeleka

        """

        self.tile_type = tile_type
        self.entity_on = entity_on
        self.walkable = walkable
        self.on_enter = on_enter
        self.on_exit = on_exit
    
    # funkcja zwracająca typ kafelka
    def get_type(self) -> str:
        return f"{self.tile_type}"

    # czy można na niego wejść
    def is_walkable(self) -> bool:
        return self.walkable and self.entity_on is None
    
    # działanie na wejściu
    def action_on_enter(self, entity):
        if self.on_enter:
            return self.on_enter(entity)
            
    # działanie na wyjściu
    def action_on_exit(self, entity):
        if self.on_exit:
            return self.on_exit(entity)
    
    # byt znajdujący się na kafelku
    def get_entity(self):
        return self.entity_on

    # ustawianie bytu na kafelku
    def set_entity(self, entity) -> None:
        self.entity_on = entity