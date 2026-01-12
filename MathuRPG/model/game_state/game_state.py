from ..combat.battle_mode import BattleMode

# klasa stanu gry (stan gry przechodzi w tryby eksploracja -> walka -> eksploracja)
class GameState:
    BATTLE = "battle" # tryb stanu gry - walka - zadania matematyczne
    EXPLORATION = "exploration" # tryb stanu gry - eksploracja - free roam

    def __init__(self) -> None: 
        self.mode = GameState.EXPLORATION # domyślny stan gry to eksploracja
        self.battle = None # brak walki 

    # rozpoczęcie walki
    def start_battle(self, player, enemy) -> None:

        """
        Docstring for start_battle
        
        :param player: callback do gracza, który kolidował z przeciwnikiem ma uczestniczyć w walce
        :param enemy: callback do przeciwnika, z którym była kolizja i ma uczestniczyć w walce

        """

        if self.is_in_battle(): # zabezpieczenie przed rozpoczęciem walki kiedy gra jest już w trybie walki
            return
        self.battle = BattleMode(player, enemy) # rozpoczęcie walki
        self.mode = GameState.BATTLE # zmiana trybu gry z eksploracji na walkę

    # zakończenie walki
    def end_battle (self) -> None:
        self.battle = None # brak aktualnej walki
        self.mode = GameState.EXPLORATION # po zakończeniu walki powrót trybu do eksploracji

    # czy właśnie trwa bitwa
    def is_in_battle(self) -> bool:
        return self.mode == GameState.BATTLE