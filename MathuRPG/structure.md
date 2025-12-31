model/
 ├─ entities/
 │   ├─ __init__.py
 │   ├─ entity.py        # klasa bazowa
 │   ├─ player.py
 │   ├─ enemy.py
 │   └─ npc.py
 │
 ├─ world/
 │   ├─ __init__.py
 │   ├─ tile.py
 │   ├─ map.py
 │   └─ chunk.py         # (jeśli proceduralna mapa)
 │
 ├─ combat/
 │   ├─ __init__.py
 │   ├─ stats.py
 │   ├─ damage.py
 │   └─ math_attack.py   # mechanika matematyczna
 │
 ├─ quests/
 │   ├─ __init__.py
 │   ├─ quest.py
 │   └─ dialogue.py
 │
 └─ game_state.py        # globalny stan gry
