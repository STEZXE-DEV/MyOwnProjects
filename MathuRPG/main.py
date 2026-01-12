import pygame, random

from model.world.map import Map
from model.world.tile import Tile
from model.game_state import GameState
from model.entities.player import Player
from model.entities.enemy import Enemy
from model.math_problems.task_generator import generate_task
from view.exploration_view import ExplorationView


def update():
    return pygame.time.get_ticks()


pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MathuRPG: Call of the Cosinus")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 32)
input_font = pygame.font.SysFont("Arial", 28)

game_state = GameState()
view = ExplorationView(screen)

# TWORZENIE MAPY

grass = Tile("grass", True)
wall = Tile("wall", False)
game_map = Map(10, 10, grass)

player = Player(1, 1)
enemy1 = Enemy(4, 4)
enemy2 = Enemy(3, 8)
enemies = [enemy1, enemy2]

game_map.get_tile(1, 1).set_entity(player)
game_map.get_tile(4, 4).set_entity(enemy1)
game_map.get_tile(3, 8).set_entity(enemy2)
game_map.set_tile(3, 4, wall)
game_map.set_tile(5, 4, wall)
game_map.set_tile(6, 2, wall)
game_map.set_tile(3, 3, wall)


current_task = None
task_surface = None
rand_enemy_move = None
last_enemy_move = 0

ENEMY_MOVE_DELAY = 1000 # milisekund opóźnienia wroga

# PĘTLA GŁÓWNA
running = True
while running:
    delta_time = clock.tick(60)
    delta_time
    now = update()
    view.draw_all(game_map)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
        # TRYB EKSPLORACJI
        if game_state.mode == game_state.EXPLORATION:
            if event.type == pygame.KEYDOWN:
                dx = dy = 0
                if event.key == pygame.K_w: dy = -1
                if event.key == pygame.K_s: dy = 1
                if event.key == pygame.K_a: dx = -1
                if event.key == pygame.K_d: dx = 1

                if dx or dy:
                    old_tile = game_map.get_tile(player.x, player.y)
                    next_move = game_map.try_move(player, dx, dy)
                    next_tile = game_map.get_tile(player.x + dx, player.y + dy)
                    print(next_move)
                    print(game_state.mode)
                    if next_move:
                        if next_move.entity_type == "Enemy":
                            enemy_in_battle = next_move
                            game_state.start_battle(player, enemy_in_battle)
                        else:
                            old_tile.set_entity(None)
                            player.move(dx, dy)
                            next_tile.set_entity(player)
                    view.draw_all(game_map)
        
            
                # for y in range(game_map.height):  #test 
                #     for x in range(game_map.width):
                #        print(x, y, game_map.get_tile(x,y).entity_on.entity_type if game_map.get_tile(x,y).entity_on is not None else None, end="\t")
                #     print(x, y, game_map.get_tile(x,y).entity_on.entity_type if game_map.get_tile(x,y).entity_on is not None else None)

            # losowy ruch przeciwnika, jeśli trafi na gracza rozpoczyna się walka
                print(last_enemy_move)
                for enemy in enemies:
                    rand_enemy_move = random.randint(1, 10)
                    if rand_enemy_move:
                        e_dx = e_dy = 0
                        if rand_enemy_move == 1: e_dy = -1 
                        if rand_enemy_move == 2: e_dy = 1
                        if rand_enemy_move == 3: e_dx = -1
                        if rand_enemy_move == 4: e_dx = 1
                    if now - last_enemy_move <= ENEMY_MOVE_DELAY:
                        last_enemy_move = now + update() 
                        if e_dx or e_dy:
                            e_old_tile = game_map.get_tile(enemy.x, enemy.y)
                            e_new_tile = game_map.try_move(enemy, e_dx, e_dy)
                            e_next_tile = game_map.get_tile(enemy.x + e_dx, enemy.y + e_dy)
                            if e_new_tile is True:
                                e_old_tile.set_entity(None)
                                enemy.move(e_dx, e_dy)
                                e_new_tile.set_entity(enemy)
                            if isinstance(e_new_tile, Player):
                                if e_new_tile.entity_type == "Player":
                                    player_in_battle = e_new_tile
                                    game_state.start_battle(player_in_battle, enemy)
                            view.draw_all(game_map)
    pygame.display.flip()
pygame.quit()