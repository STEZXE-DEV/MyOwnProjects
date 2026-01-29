# klasa trybu bitwy
class BattleMode:
    def __init__(self, player, enemy) -> None:

        """
        Docstring for __init__
        
        :param player: callback do gracza
        :param enemy: callback do przeciwnika

        """

        self.player = player
        self.enemy = enemy
        self.winner = None # To może się przydać później do komunikatów typu "Wygrałeś"/"Przegrałeś"

    # funkcja zadania obrażeń
    def deal_damage(self, attacker, defender) -> None:

        """
        Docstring for deal_damage
        
        :param attacker: callback do bytu (gracza lub przeciwnika), który zada obrażenia
        :param defender: callback do bytu (gracza lub przeciwnika), który otrzyma obrażenia
        :param amount: ilość obrażeń, które zostaną zadane

        """
        amount = attacker.power * 2

        # if attacker.entity_type == "Player": - może się przydać potem

        # conclusion jest elementem tylko w klasie Player
        amount = max(0, amount - getattr(defender, 'conclusion', 0)) # ilość obrażeń nie może być mniejsza od 0

        # jeden punkt mocy (power) to 2HP obrażeń
        if amount:
            defender.take_damage(amount)

    # działanie po odpowiedzi użytkownika w zależności od jej poprawności z zadaniem i czasem
    def action_after_player_answer(self, player_answer: str | int, task) -> None | bool:

        if player_answer is not None and player_answer.lstrip('-').isnumeric():
            player_answer = int(player_answer)
        task.submit_answer(player_answer)
        if task.is_task_done_correctly_in_time():
            self.deal_damage(self.player, self.enemy)
        else:
            self.deal_damage(self.enemy, self.player)
        return self.get_winner()

    def get_winner(self) -> str | None:
        self.winner = "Enemy" if self.player.hp <= 0 else "Player" if self.enemy.hp <= 0 else None
        return self.winner
