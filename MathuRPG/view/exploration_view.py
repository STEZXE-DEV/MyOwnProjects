import pygame

# klasa widoku eksploracji
class ExplorationView:
    def __init__(self, screen, tile_size=64):
        self.screen = screen
        self.tile_size = tile_size
    
    def draw_entity(self, width, height, entity):
        color = None
        if entity.entity_type == "Player":
            color = (0, 0, 255)
        if entity.entity_type == "Enemy":
            color = (255, 0, 0)
        pygame.draw.circle(
                        self.screen, color,
                        (width*self.tile_size+32, height*self.tile_size+32), 20
                    )


    def draw_tile(self, width, height, tile):
        if tile.tile_type == "grass":
            color = (100, 200, 100) 
        if tile.tile_type == "wall":
            color = (80, 80, 80)
        pygame.draw.rect(
            self.screen, 
            color,
            (width*self.tile_size, height*self.tile_size, self.tile_size, self.tile_size)
        )


    # rysowanie mapy i obiektów gry na ekranie
    def draw_all(self, game_map) -> None:
        for height in range(game_map.height):
            for width in range(game_map.width):
                tile = game_map.get_tile(width, height)
                if tile:
                    self.draw_tile(width, height, tile)
                entity = tile.get_entity()
                if entity:
                    self.draw_entity(width, height, entity)
                    

