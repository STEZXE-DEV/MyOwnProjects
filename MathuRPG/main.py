import pygame as pg
from model.math_problems.tasks_generators import *
import pygame

class InputBox:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('gray')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = ""
        self.font = font
        self.txt_surface = font.render(self.text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Kliknięcie — aktywacja pola
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print("Zatwierdzono:", self.text)
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, pygame.Color('black'))

    def draw(self, screen):
        # Rysuj tekst
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Rysuj ramkę
        pygame.draw.rect(screen, self.color, self.rect, 2)

question, correct_ans = generate_basic_equation_task(2)

pg.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
CAPTION = "MathuRPG: Call of the Cosinus"
COLOR_BOX = (10,10,210)
screen = pg.display.set_mode(RESOLUTION, pg.SHOWN)
window_caption = pg.display.set_caption(CAPTION)
clock = pg.time.Clock()
speed = 5
x=0
y=0
SIZE_X = 200
SIZE_Y = 200

running = True

input_font = pygame.font.SysFont("Arial", 28)
input_box = InputBox(SCREEN_WIDTH//2 - 200 , SCREEN_HEIGHT//2 + 75, 400, 40, input_font)
font = pg.font.SysFont("Times New Roman", 36)
text = font.render(question, True, "black")

# utworzenie nowej powierzchni do rysowania (szerokość wysokość)
surface = pg.Surface((SIZE_X, SIZE_Y)) 
surface.fill(COLOR_BOX) # wypełnienie kolorem

# pętla aplikacji
while running: 
    clock.tick(60) #60 FPS

    for i in pg.event.get():
        if i.type == pg.QUIT:
            running = False
        input_box.handle_event(i)

# akcja
    keys=pg.key.get_pressed() #musi być wewnątrz running
    if keys[pg.K_w] and y >= 0:
        y -= speed
    if keys[pg.K_s] and y <= (SCREEN_HEIGHT - SIZE_Y):
        y += speed
    if keys[pg.K_a] and x >= 0:
        x -= speed
    if keys[pg.K_d] and x <= (SCREEN_WIDTH - SIZE_X):
        x += speed

# rysowanie gry
    #wypełnienie tłem
    screen.fill(color=(0,200,100))

    # umieszczenie na tle nowej powierzchni na (x,y)
    # punkt pierotny (0,0) znajduje się w lewym górnym rogu
    # prawidłowa kolejność rysowania: najpierw to co na spodzie
    screen.blit(surface, (x, y))
    screen.blit(text, (250, SCREEN_HEIGHT//2))
    input_box.draw(screen)

    pg.display.update() #przerysowanie ekranu




pg.quit()