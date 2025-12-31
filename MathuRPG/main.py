import pygame as pg

pg.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
CAPTION = "MathuRPG: Call of the Cosinus"
COLOR_BOX = (10,10,210)
screen = pg.display.set_mode(RESOLUTION, pg.SHOWN)
window_caption = pg.display.set_caption(CAPTION)
clock = pg.time.Clock()
speed = 25
x=0
y=0
SIZE_X = 200
SIZE_Y = 200

running = True

# utworzenie nowej powierzchni do rysowania (szerokość wysokość)
surface = pg.Surface((SIZE_X, SIZE_Y)) 
surface.fill(COLOR_BOX) # wypełneinie kolorem

# pętla aplikacji
while running: 
    clock.tick(60) #60 FPS

    for i in pg.event.get():
        if i.type == pg.QUIT:
            running = False

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

    pg.display.update() #przerysowanie ekranu




pg.quit()