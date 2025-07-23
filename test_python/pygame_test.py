import pygame

pygame.init()

game_screen = pygame.display.set_mode((600, 500))
is_running = True
image_test = pygame.image.load("cardClubs4.png")

surface_load = []

size = (200, 200)
position_x_coordinate = game_screen.get_width() // 2 - (size[0] // 2)
position_y_coordinate = game_screen.get_height() // 2 - (size[1] // 2)
table_border_rect = pygame.Rect(position_x_coordinate, position_y_coordinate, size[0], size[1])

table_border_color = '0x7B3F00'

table_border = (table_border_color, table_border_rect)
surface_load.append(table_border)

table_fill_color =  '0x35654D'
size = (188, 188)
position_x_coordinate = game_screen.get_width() // 2 - (size[0] // 2)
position_y_coordinate = game_screen.get_height() // 2 - (size[1] // 2)
table_fill_rect = pygame.Rect(position_x_coordinate, position_y_coordinate, size[0], size[1])
table_fill = (table_fill_color, table_fill_rect)
surface_load.append(table_fill)

def frame_update(load_order):
    game_background_color = '0x80001f'
    game_screen.fill(game_background_color)

    for surface in load_order:
        pygame.draw.rect(game_screen, surface[0], surface[1])


card_position = [20.0, 20.0]
card_destination_x = game_screen.get_width() // 2 - (image_test.get_width() // 2)
card_destination_y = game_screen.get_height() // 2 - (image_test.get_height() // 2)
card_destination = (card_destination_x, card_destination_y)
rate = 0.015

while is_running:
    card_position[0] = card_position[0] + (card_destination_x - card_position[0]) * rate
    card_position[1] = card_position[1] + (card_destination_y - card_position[1]) * rate
    frame_update(surface_load)
    game_screen.blit(image_test, card_position)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    pygame.display.flip()

    
pygame.quit()

