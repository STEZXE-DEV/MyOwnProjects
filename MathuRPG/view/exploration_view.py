import pygame

class ExplorationView:
    def __init__(self, screen, tile_size=64):
        self.screen = screen
        self.tile_size = tile_size
        self.font = pygame.font.SysFont("Arial", 20)

    def draw_entity(self, width, height, entity, offset_x, offset_y):
        if not entity.is_alive():
            return

        if entity.entity_type == "Player":
            color = (0, 0, 255)
        elif entity.entity_type == "Enemy":
            color = (255, 0, 0)
        else:
            return

        pygame.draw.circle(
            self.screen,
            color,
            (width * self.tile_size + self.tile_size // 2 + offset_x,
             height * self.tile_size + self.tile_size // 2 + offset_y),
            20
        )

    def draw_tile(self, width, height, tile, offset_x, offset_y):
        if tile.tile_type == "grass":
            color = (100, 200, 100)
        elif tile.tile_type == "wall":
            color = (80, 80, 80)
        else:
            color = (0, 0, 0)

        pygame.draw.rect(
            self.screen,
            color,
            (width * self.tile_size + offset_x,
             height * self.tile_size + offset_y,
             self.tile_size,
             self.tile_size)
        )

    def draw_hud(self, player):
        # ramka
        pygame.draw.rect(self.screen, (0, 0, 0), (20, 20, 204, 24), 2)

        # pasek HP
        hp_ratio = player.hp / player.max_hp
        hp_width = int(200 * hp_ratio)

        pygame.draw.rect(
            self.screen,
            (200, 50, 50),
            (22, 40, hp_width, 20)
        )

        # tekst
        text = self.font.render(
            f"HP: {player.hp}/{player.max_hp}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(text, (22, 65))

    def draw_all(self, game_map, player) -> None:
        self.screen.fill((0, 0, 0)) # wypełnienie kolorem czarnym

        # obliczanie przesunięcia, żeby wycentrować mapę
        map_pixel_width = game_map.width * self.tile_size
        map_pixel_height = game_map.height * self.tile_size
        offset_x = self.screen.get_width() // 2 - map_pixel_width // 2
        offset_y = self.screen.get_height() // 2 - map_pixel_height // 2

        # rysowanie kafelków i bytów
        for height in range(game_map.height):
            for width in range(game_map.width):
                tile = game_map.get_tile(width, height)
                if tile:
                    self.draw_tile(width, height, tile, offset_x, offset_y)

                entity = tile.get_entity()
                if entity:
                    self.draw_entity(width, height, entity, offset_x, offset_y)

        # HUD
        self.draw_hud(player)
