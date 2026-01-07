import random as r
from .utils import DIFFICULTY_LEVELS
from .arithmetic_task import generate_arithmetic_task as gen_arithmetic
from .simple_equation_task import generate_basic_equation_task as gen_equation


TASK_GEN_FUNCTIONS = [gen_arithmetic, gen_equation] # jeszcze nie ma gen_geometry, gen_square_fn, gen_trigonometry + innych 

# funkcja generująca zadanie wedle poziomu przeciwnika i poziomu trudności gry
def generate_task(enemy_level, game_difficulty): # task_type będzie z enemy.level (max 5 lub 10 zależy ile mi się uda), task_difficulty będzie brany z poziomu trudności gry (1, 2, 3)
    for k, v in enumerate(TASK_GEN_FUNCTIONS, 1):
        if k == enemy_level:
            task_gen = v
    for k, v in enumerate(DIFFICULTY_LEVELS, 1):
        if k == game_difficulty:
            task_level = game_difficulty
    return task_gen(task_level)