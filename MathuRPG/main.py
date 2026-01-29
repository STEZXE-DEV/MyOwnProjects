import pygame, random

from model.world.map import Map
from model.world.tile import Tile
from model.game_state import GameState
from model.entities.player import Player
from model.entities.enemy import Enemy

from model.math_problems.task_generator import generate_task
from model.math_problems.math_task import MathTask

from view.exploration_view import ExplorationView
from view.battle_view import BattleView
from view.game_over_view import GameOverView


def tick_update():
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
battle_view = BattleView(screen)
game_over_view =  GameOverView(screen)

# TWORZENIE MAPY

grass = Tile("grass", True)
wall = Tile("wall", False)
game_map = Map(10, 10, grass)

player = Player(1, 1)
enemy1 = Enemy(4, 4, level=1)
enemy2 = Enemy(3, 8, level=2)
enemies = [enemy1, enemy2]

game_map.get_tile(1, 1).set_entity(player)
game_map.get_tile(4, 4).set_entity(enemy1)
game_map.get_tile(3, 8).set_entity(enemy1)
for _ in range(10):
    rng_x = random.randint(0, 9) 
    rng_y = random.randint(0, 9)
    rng_tile =  game_map.get_tile(rng_x, rng_y)
    if rng_tile.entity_on is None:
        game_map.set_tile(rng_x, rng_y, wall)



current_task = None
task_surface = None
rand_enemy_move = None
last_enemy_move = 0
collided_enemy = None
difficulty_level = "NORMAL"
winner = None

ENEMY_MOVE_DELAY = 1000 # milisekund opóźnienia wroga

# PĘTLA GŁÓWNA
running = True
while running:
    delta_time = clock.tick(60)
    now = tick_update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
  
        # TRYB EKSPLORACJI
        # jeśli stan gry to eksploracja gracz oraz przeciwnicy mogą się poruszać, jeśli rozpocznie się walka byty zastygają
        if game_state.mode == game_state.EXPLORATION:
            delta_time = clock.tick(60)
            if len(enemies) == 0:
                winner = "Player"
                game_state.game_end()
            view.draw_all(game_map, player)
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
                    
                    # print(next_move)
                    # print(game_state.mode)

                    if next_move:
                        if next_move.entity_type == "Enemy":
                            
                            collided_enemy = next_move
                            current_task = generate_task(collided_enemy.level, difficulty_level)
                            current_task_qst, current_task_ans  = generate_task(collided_enemy.level, difficulty_level)
                            
                            enemy_in_battle = next_move
                            game_state.start_battle(player, collided_enemy)
                        else:
                            old_tile.set_entity(None)
                            player.move(dx, dy)
                            next_tile.set_entity(player)
                    view.draw_all(game_map, player)
        
            
                # for y in range(game_map.height):  #test rozmieszczenia bytów
                #     for x in range(game_map.width):
                #        print(x, y, game_map.get_tile(x,y).entity_on.entity_type if game_map.get_tile(x,y).entity_on is not None else None, end="\t")
                #     print(x, y, game_map.get_tile(x,y).entity_on.entity_type if game_map.get_tile(x,y).entity_on is not None else None)

            # losowy ruch przeciwnika, jeśli trafi na gracza rozpoczyna się walka
                # print(last_enemy_move)
                for enemy in enemies:
                    rand_enemy_move = random.randint(0, 11)
                    e_dx = e_dy = 0
                    if rand_enemy_move:
                        if rand_enemy_move == 1: e_dy = -1 
                        if rand_enemy_move == 2: e_dy = 1
                        if rand_enemy_move == 3: e_dx = -1
                        if rand_enemy_move == 4: e_dx = 1
                        if rand_enemy_move in (5,6): e_dx, _ = enemy.follow_target(player)
                        if rand_enemy_move in (7,8): _, e_dy = enemy.follow_target(player)
                        if rand_enemy_move in (10, 11): e_dx, e_dy = enemy.follow_target(player)
                        # if rand_enemy_move == 10: e_dx, _ = enemy.follow_target(player, 2) # skok o 2
                        # if rand_enemy_move == 11: _, e_dy = enemy.follow_target(player, 2)

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
                                    
                                    collided_enemy = enemy
                                    current_task_qst, current_task_ans  = generate_task(collided_enemy.level, difficulty_level)

                                    # print(current_task)

                                    player_in_battle = e_new_tile
                                    game_state.start_battle(player_in_battle, enemy)
                                    # print(game_state.mode)
                            view.draw_all(game_map, player)
        
        # TRYB WALKI
        elif game_state.mode == GameState.BATTLE:
            delta_time = clock.tick(60)
            current_task = MathTask(current_task_qst, current_task_ans, 100)
            battle_view.draw_all(player, collided_enemy, current_task)
            answer = battle_view.handle_event(event)
            if answer is not None and answer != "":
                game_state.battle.action_after_player_answer(answer, current_task)
                if not collided_enemy.is_alive():
                    enemies.remove(collided_enemy)
                    dead_enemy_tile = game_map.get_tile(collided_enemy.x, collided_enemy.y)
                    dead_enemy_tile.entity_on = None
                    game_state.end_battle()

                elif not player.is_alive():
                    winner = game_state.battle.get_winner()
                    game_state.end_battle()
                    game_state.game_end()

                else:
                    current_task_qst, current_task_ans  = generate_task(collided_enemy.level, difficulty_level)
                    current_task = MathTask(current_task_qst, current_task_ans, 100)
        
        elif game_state.mode == GameState.END:
            game_over_view.draw_all(winner)
                    
    pygame.display.flip()
pygame.quit()
