import pygame

clock = pygame.time.Clock()
# font = pygame.font.SysFont("Arial", 32)

class InputBox:
    active_color = pygame.Color(200,200,200)
    inactive_color = pygame.Color(175,175,175)
    def __init__(self, x , y, w, h, font):
        self.rect = pygame.Rect(x,y,w,h)
        self.font = font
        self.input = ""
        self.active = False
    
    def handle_user_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.input = self.input[:-1]
            elif event.key == pygame.K_DELETE:
                self.input = ""
            elif event.key == pygame.K_RETURN:
                confirmed_input = self.input
                self.input = ""
                return confirmed_input
            else:
                self.input += event.unicode


    def draw_input_box(self, screen):
        if self.active == True:
            self.color = InputBox.active_color
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, (0, 110, 255), self.rect, 2)
        elif self.active == False:
            self.color = InputBox.inactive_color 
            pygame.draw.rect(screen, self.color, self.rect) 
            pygame.draw.rect(screen, (0,0,0), self.rect, 1) 
        text_surface = self.font.render(self.input, True, (0,0,0))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))
        

# input_box = InputBox(300, 170, 200, 50, font)

# running = True
# while running:
#     clock.tick(60)
#     screen.fill((240, 240, 240))

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         input_box.handle_user_input(event)
#     input_box.draw_input_box(screen)
#     pygame.display.flip()

    