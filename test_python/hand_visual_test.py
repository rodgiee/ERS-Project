import pygame

class Image():
    def __init__(self, x, y, angle, surface):
        self.x = x
        self.y = y
        self.angle = angle
        self.surface = surface
        self.size = [self.surface.get_width(), self.surface.get_height()]
        
def frame_background_update(load_order):
    game_background_color = '0x80001f'
    game_screen.fill(game_background_color)

    for surface in load_order:
        pygame.draw.rect(game_screen, surface[0], surface[1])

scale_test = 1
def hand_update(screen, image):
    # 160, 500 initial
    # 160, 120 destination
    #destination_x = 160
    #destination_y = 120
    #rate = 0.02
    #image.x = image.x + (destination_x - image.x) * rate
    #image.y = image.y + (destination_y - image.y) * rate

    image.y=120
    global scale_test
    scale_test -= 0.001
    rescaled = pygame.transform.smoothscale_by(image.surface, scale_test)
    rescaled.get_rect(center=image.surface.get_rect()).center = image.surface.get_rect().center
    
    #image.surface= pygame.transform.smoothscale_by(image.surface, 0.999999)
    
    #screen.blit(image.surface, (image.x, image.y))
    screen.blit(rescaled, (image.x, image.y))

pygame.init()

game_screen = pygame.display.set_mode((599, 500))
is_running = True

surface_load = []

size = (200, 200)
x = game_screen.get_rect().centerx - (size[0] // 2)
y = game_screen.get_rect().centery - (size[1] // 2)
item_rect = pygame.Rect(x, y, size[0], size[1])
item_color = '0x7B3F00'
item = (item_color, item_rect)

surface_load.append(item)

size = (188, 188)
x = game_screen.get_rect().centerx - (size[0] // 2)
y = game_screen.get_rect().centery - (size[1] // 2)
item_rect = pygame.Rect(x, y, size[0], size[1])
item_color =  '0x35654D'
item = (item_color, item_rect)
surface_load.append(item)

# IMAGE STUFF
# ----------
hand_image = pygame.image.load('images/slap.png')
hand = Image(160, 500, 0, hand_image)

while is_running:
    # load in floor and table
    frame_background_update(surface_load)

    #change_x = int(input('input x:'))
    #change_y = int(input('input y:'))

    hand_update(game_screen, hand)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())


    pygame.display.flip()

    
pygame.quit()

