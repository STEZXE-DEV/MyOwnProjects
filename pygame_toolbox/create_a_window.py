import pygame as pg

pg.init()

#resolution must be a tuple!
resolution = (800, 800) #that means 800x800 window
screen = pg.display.set_mode(resolution)

running = True

#essential loop for closing the application with "x"
while running: 
    for i in pg.event.get():
        if i.type == pg.QUIT:
            running = False

pg.quit()