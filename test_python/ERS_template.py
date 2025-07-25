import pygame
        
def frame_background_update(load_order):
    game_background_color = '0x80001f'
    game_screen.fill(game_background_color)

    for surface in load_order:
        pygame.draw.rect(game_screen, surface[0], surface[1])

pygame.init()

game_screen = pygame.display.set_mode((600, 500))
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

while is_running:
    # load in floor and table
    frame_background_update(surface_load)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())


    pygame.display.flip()

    
pygame.quit()

