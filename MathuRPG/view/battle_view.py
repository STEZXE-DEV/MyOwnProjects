import pygame
from view.input_box import InputBox   

class BattleView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 32)
        self.small_font = pygame.font.SysFont("Arial", 24)

        self.input_box = InputBox(
            x=screen.get_width() // 2 - 100,
            y=screen.get_height() // 2 + 40,
            w=200,
            h=50,
            font=self.font
        )

    # ---------- EVENTY ----------
    def handle_event(self, event):
        # zwraca odpowiedź gracza w str albo None
        return self.input_box.handle_user_input(event)

    # ---------- RYSOWANIE ----------
    def draw_all(self, player, enemy, task):
        self.screen.fill((50, 50, 50))

        self.draw_panels()
        self.draw_entities(player, enemy)
        self.draw_hp(player, enemy)
        self.draw_task(task)

        self.input_box.draw_input_box(self.screen)

    def draw_panels(self):
        panel_w, panel_h = 900, 500
        x = self.screen.get_width() // 2 - panel_w // 2
        y = self.screen.get_height() // 2 - panel_h // 2


        pygame.draw.rect(self.screen, (222, 222, 222), (x, y, panel_w, panel_h))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, panel_w, panel_h), 2)

        self.panel_x = x
        self.panel_y = y
        self.panel_width = panel_w
        self.panel_height = panel_h
        self.panel_center_x =  self.panel_width // 2 + self.panel_x


    def draw_entities(self, player, enemy):
        py = self.panel_y + 200
        
        pygame.draw.circle(self.screen, (0, 0, 255),
                        (self.panel_center_x - 300 , py), 30)

        pygame.draw.circle(self.screen, (200, 50, 50),
                        (self.panel_center_x + 300  , py), 30)


    def draw_hp(self, player, enemy):
        # Player HP
        self.draw_hp_bar(self.panel_center_x - 102 - 300, self.panel_y + 125, player.hp, player.max_hp, "Player")
        # Enemy HP
        self.draw_hp_bar(self.panel_center_x - 102 + 300, self.panel_y + 125, enemy.hp, enemy.max_hp, f"Enemy (lvl. {enemy.level})")

    def draw_hp_bar(self, x, y, hp, max_hp, label):
        ratio = hp / max_hp
        pygame.draw.rect(self.screen, (0, 0, 0), (x , y, 204, 24), 2)
        pygame.draw.rect(self.screen, (200, 50, 50), (x + 2, y + 2, int(200 * ratio), 20))

        text = self.small_font.render(f"{label}: {hp}/{max_hp}", True, (0, 0, 0))
        self.screen.blit(text, (x, y - 25))

    def draw_task(self, task):
        text = self.font.render(task.question, True, (0, 0, 0))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.panel_y + 10))
