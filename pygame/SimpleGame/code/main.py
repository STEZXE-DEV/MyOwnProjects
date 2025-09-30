import pygame
import random as r

def losuj(start, end):
    return r.randint(start, end)

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SimpleGame.exe")

# Gracz
x, y = 350, 500
speed = 5
player_size = 25

# Przeszkody
obstacles = []
for _ in range(5):  # 5 przeszkód na start
    obstacles.append([losuj(0, width-80), losuj(-600, 0)])

obs_speed = 3

# Punkty
score = 0
font = pygame.font.SysFont("Arial", 30)

running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60)  # 60 FPS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Sterowanie
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x += speed

    # Granice ekranu
    x = max(0, min(x, width - player_size))

    screen.fill((30,30,30))

    # Gracz
    player = pygame.draw.rect(screen, (0, 200, 0), (x, y, player_size, player_size))

    # Rysowanie przeszkód
    for obs in obstacles:
        obs[1] += obs_speed  # przeszkoda spada
        obstacle = pygame.draw.rect(screen, (200, 0, 0), (obs[0], obs[1], 40, 40))

        # Sprawdź kolizję
        if player.colliderect(obstacle):
            print("GAME OVER! Wynik:", score)
            running = False

        # Reset przeszkody
        if obs[1] > height:
            obs[0] = losuj(0, width-80)
            obs[1] = losuj(-200, -50)
            score += 1  # +1 punkt za ominięcie

    # Wyświetl wynik
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Utrudnianie gry
    max_speed = 8  # nigdy szybciej niż 8
    obs_speed = min(max_speed, 3 + score // 15)

    # Dodawanie przeszkód co 20 punktów
    if score % 20 == 0 and score > 0 and len(obstacles) < 10:
        obstacles.append([losuj(0, width-80), losuj(-200, -50)])



    pygame.display.flip()

pygame.quit()
