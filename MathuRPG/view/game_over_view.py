import pygame


class GameOverView:
    def __init__(self, screen):
        self.screen = screen
        self.big_font = pygame.font.SysFont("Arial", 72, bold=True)
        self.medium_font = pygame.font.SysFont("Arial", 36)
        self.small_font = pygame.font.SysFont("Arial", 24)

    def draw_all(self, winner: str | None):
        # tło
        self.screen.fill((0, 0, 0))
        player_win_color = (50, 220, 50)
        player_win_text = "YOU WIN!"
        enemy_win_color = (220, 50, 50)
        enemy_win_text = "GAME OVER"

        #  zwycięzca
        if winner:
            if winner.lower() == "player":
                color = player_win_color
                text = player_win_text
            
            elif winner.lower() == "enemy":
                color = enemy_win_color
                text = enemy_win_text
            
            title_text = self.big_font.render(text, True, color)
            self.screen.blit(
                title_text,
                (
                    self.screen.get_width() // 2 - title_text.get_width() // 2,
                    150
                )
            )
                
            winner_text = self.medium_font.render(
                f"Winner: {winner}",
                True,
                (255, 255, 255)
            )
            self.screen.blit(
                winner_text,
                (
                    self.screen.get_width() // 2 - winner_text.get_width() // 2,
                    260
                )
            )

        # tekst na dole
        hint_text = self.small_font.render(
            "Press ESC to quit",
            True,
            (180, 180, 180)
        )
        self.screen.blit(
            hint_text,
            (
                self.screen.get_width() // 2 - hint_text.get_width() // 2,
                340
            )
        )
