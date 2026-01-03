# Architektura MVC – gra matematyczna (Pygame)

## Model
model/
 ├─ entities/
 │   ├─ entity.py
 │   ├─ player.py
 │   └─ enemy.py
 ├─ world/
 │   ├─ tile.py
 │   ├─ map.py
 │   └─ chunk.py
 ├─ combat/
 │   ├─ stats.py
 │   └─ damage.py
 ├─ math_problems/
 │   ├─ math_task.py
 │   └─ tasks_generators.py
 └─ game_state.py

## View
view/
 ├─ renderer.py
 ├─ ui.py
 └─ assets/

## Controller
controller/
 ├─ input_handler.py
 ├─ combat_controller.py
 └─ game_controller.py

## main.py
Punkt startowy gry.

