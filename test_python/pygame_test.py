import pygame
import random
class Card():
    def __init__(self, x, y, angle, image):
        self.x = x
        self.y = y
        self.angle = angle
        self.image = image
        
def pick_random_card_image():
    suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
    image_file = f'images/card{random.choice(suits)}{random.choice(values)}.png'
    image = pygame.image.load(image_file)
    return image

def move_card(card):
    # move image
    destination_x = game_screen.get_rect().centerx 
    destination_y = game_screen.get_rect().centery
    rate = 0.02
    card.x = card.x + (destination_x - card.x) * rate
    card.y = card.y + (destination_y - card.y) * rate

    #rotate image
    tolerance = 10
    x_bound = destination_x - tolerance <= card.x <= destination_x + tolerance
    y_bound = destination_y - tolerance <= card.y <= destination_y + tolerance
    if (not(x_bound and y_bound )):
        x_factor = abs(destination_x - abs(card.x)) / destination_x
        y_factor = abs(destination_y - abs(card.y)) / destination_y
        card.angle += 2 * (x_factor + y_factor) 
    rotated_image = pygame.transform.rotate(card.image, card.angle)
    rotated_image_rect = rotated_image.get_rect(center= (card.x, card.y))
    
    game_screen.blit(rotated_image, rotated_image_rect)



def frame_background_update(load_order):
    game_background_color = '0x80001f'
    game_screen.fill(game_background_color)

    for surface in load_order:
        pygame.draw.rect(game_screen, surface[0], surface[1])

pygame.init()

game_screen = pygame.display.set_mode((600, 500))
is_running = True
image_test = pygame.image.load("images/cardClubs8.png")

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

cards = []
cards.append(Card(20, 20, 0, image_test))
while is_running:
    # load in floor and table
    frame_background_update(surface_load)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            cards.append(Card(mouse_position[0], mouse_position[1], random.random() * 360, pick_random_card_image()))


    for card in cards:
        move_card(card)

    if (len(cards) > 15): cards.pop(0)
    
    pygame.display.flip()

    
pygame.quit()

