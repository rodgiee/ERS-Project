import pygame
import random
import time
import threading
import os

def move_card(game_screen, card):
    # move image
    destination_x = game_screen.get_rect().centerx 
    destination_y = game_screen.get_rect().centery
    rate = 0.03
    #print(card.x,card.y)
    #print(card.owner.position)
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

def game_handler(game_players):
    # game loop main conditional
    # also used by game_visual_handler() to see if game is finished --> closes out if so
    # game_current_player_id checks who's turn is it 
    global is_game_running
    game_current_player_id = 0

    # mutex lock for game_deck to prevent race conditions
    global deck_lock
    deck_lock = threading.Lock()
    
    # detects if there is either a "sandwich" or "pair", used to check if the player slapped correctly or not
    # used by slap() to verify
    global is_pattern
    is_pattern = False

    global game_turn_finished

    #clear initalization checks
    time.sleep(1)
    os.system('clear')
    


    # game loop
    while (is_game_running):
        check_game(game_players)

        game_turn_finished = False

        # initalize player threads, each player will have its own independent thread process to simulate simultaneous player behavior
        # needs to be in loop since "threads can only be started once"
        thread_players = []

        for player_index in range(len(game_players)):
            thread_players.append(threading.Thread(target=control_player, args=(game_current_player_id, game_players[player_index], player_index)))

        print(f'{game_players[game_current_player_id]}')
        for player_thread in thread_players:
            player_thread.start()

        for player_thread in thread_players:
            player_thread.join()

        game_current_player_id = (game_current_player_id + 1) %  len(game_players)
    
def check_game(game_players):
    global is_game_running
    for player in game_players:
        if len(player.inventory) >= 48:
            print(f'{player} wins!')
            is_game_running = False
def Game():
    '''
    The main body of for ERS game
    It will first:
    2. Create the players 
    1. Initialize shuffle the deck
    3. Distribute out the cards from the deck evenly to the players
    
    
    '''
    game_main_player_name = input("What is your name?: ")
    
    global game_deck 
    game_deck = [] # initialize the game_deck of cards for this game
    game_players = [] # Initialize the players playing this game

    # Initialize all players by assigning them an id, name, position for pygame visuals
    # Bot names are randomly chosen
    random_first_names = ["Zonko", "Fizzler", "Snorple", "Quibly", "Norbix", "Jaxor", "Bloopo", "Zindle", "Crunkle", "Vexon"]
    random_last_names = ["Glimbo", "Torkel", "Zappy", "Marnix", "Flurbo", "Kazzle", "Droopo", "Wibbit", "Tronix", "Blixel"]
    print("Creating players...")
    
    game_players.append(Player(0, game_main_player_name, (300, 500))) # Create main player
    game_players.append(Player(1, random.choice(random_first_names)+random.choice(random_last_names), (0, 250))) # Create main player
    game_players.append(Player(2, random.choice(random_first_names)+random.choice(random_last_names), (300, 0))) # Create main player
    game_players.append(Player(3, random.choice(random_first_names)+random.choice(random_last_names), (600, 250))) # Create main player
    print("Players created!")
    print("(", end="", flush=True)
    for player in game_players: print(f"{str(player)}, ", end="", flush=True)
    print(")", end="", flush=True)

    # Initalize the deck with 52 cards and shuffle
    print(f"\nDeck initializing...(currently {len(game_deck)} in game_deck)")
    for suit in range(4):
        for value in range (2,14):
            game_deck.append(Card(suit, value)) # append this new card to the game_deck list
    print(f"Deck Initalized! (created {len(game_deck)} cards in game_deck)\n")

    print(f"Deck shuffling... (first card = {str(game_deck[0])})")
    random.shuffle(game_deck) # shuffle the game_deck
    print(f"Deck shuffled! (first card now = {str(game_deck[0])})\n")

    
    # Distribute the game deck of 52 cards evenly to all players
    print("\n\nDistributing cards to players...")
    game_current_player_id = 0
    while(len(game_deck) > 0):
        card = game_deck.pop(0)
        player = game_players[game_current_player_id]
        card.x = player.position[0]
        card.y = player.position[1]
        card.owner = player
        card.angle = random.random() * 360 # ensures that card animations don't end up at same angle
        game_players[game_current_player_id].inventory.append(card)
        
        game_current_player_id = (game_current_player_id + 1) % len(game_players)

    print("Distributed cards to players!")
    for player in game_players: print(f"({str(player)} has {len(player.inventory)} cards.)")

    global is_game_running
    is_game_running = True

    game_thread = threading.Thread(target=game_handler, args=(game_players,))
    game_thread.start()

    # prepare game visual window
    pygame.init()
    game_screen = pygame.display.set_mode((600, 500))

    #load table and floor
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

    global main_player_input
    main_player_input = None

    card_renderer = []

    while(is_game_running):
        # performance issues with rendering more than 10 cards
        # cap the amount of cards being displayed by only displaying the last 7 cards of the deck
        if len(game_deck) <= 7:
            card_renderer = game_deck
        else:
            card_renderer = game_deck[-7:]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_p:
                        main_player_input = 'place'
                    case pygame.K_SPACE:
                        main_player_input = 'slap'
                    case pygame.K_a:
                        print(len(game_players[0].inventory))

        game_background_color = '0x80001f'
        game_screen.fill(game_background_color)

        for surface in surface_load:
            pygame.draw.rect(game_screen, surface[0], surface[1])

        for card in card_renderer:
            #print(card.x, card.y, card.owner, card.owner.position)
            move_card(game_screen, card)

        pygame.display.flip()

    game_thread.join()
    pygame.quit()





def check_pattern():
    top_card_index = len(game_deck) - 1
    global is_pattern
    if (len(game_deck) >= 2 and (game_deck[top_card_index] == game_deck[top_card_index - 1]) ): # check for pair 
        is_pattern = True
    elif (len(game_deck) >= 3 and (game_deck[top_card_index] == game_deck[top_card_index - 2]) ): # check for sandwich
        is_pattern = True
    else:
        is_pattern = False

def slap(player_object):
    global is_pattern
    global game_deck
    if(is_pattern):
        print(f'{player_object} slaps in!')
        print(f'had {len(player_object.inventory)} cards.')
        player_object.inventory.extend(game_deck)
        game_deck = []
        print(f'now {len(player_object.inventory)} cards.')
        is_pattern = False
        

def place_card(player_object):
    # take the card from player's inventory at the last index and append to game deck
    top_card_index = len(player_object.inventory) - 1
    top_card = player_object.inventory.pop(top_card_index)
    
    deck_lock.acquire()
    game_deck.append(top_card)
    check_pattern()
    deck_lock.release()

    # not sure why but it would make main player place from right hand side (600, 250) instead of player side (300, 500)
    # below helps realign the card position to where it should go
    top_card.x = player_object.position[0]
    top_card.y = player_object.position[1]
    
    print(f'{str(player_object)} places {top_card}')

    return top_card

def control_player(game_current_player_id, player_object, player_id):
    global game_turn_finished
    global is_pattern
    if (player_id == 0): # case if main player
        while(not game_turn_finished and is_game_running):
            global main_player_input
            
            if (main_player_input in ['p', 'place'] and game_current_player_id == player_id):
                place_card(player_object)
                main_player_input = None
                game_turn_finished = True
                break
            if (main_player_input in ['s', 'slap'] and is_pattern):
                slap(player_object)
                main_player_input = None
                break
    else: # case if bot
        if (is_pattern):
            # bot will detect for patterns and slap in if detected
            # in case for race conditions we will need to do a mutex lock and re-verify if there is still a pattern
            time.sleep(random.random() * 1 + 1)
            deck_lock.acquire()
            if (is_pattern):
                slap(player_object)
            deck_lock.release()
            game_turn_finished = True

        if game_current_player_id == player_id:
            time.sleep(random.random() * 1 + 0.5 ) 
            if len(player_object.inventory) > 0:
                place_card(player_object)
            game_turn_finished = True
            
    return

class Player:
    '''
    Player = id, card inventory, name
    '''
    def __init__(self, p_id, name, position):
        self.p_id = p_id # integer player identifier
        self.inventory = [] # list of cards player holds
        self.name = name # string name of player
        self.position = position
    
    def __str__(self):
        return self.name
    
class Card:
    '''
    Card: 
    - suit - 0 = spades, 1 - clubs, 2 = hearts, 3 = diamonds
    - value - 1-9, 10(Jack), 11(Queen), 12(King), 13(Ace)
    '''
    def __init__(self, suit, value, owner =None,  x=0, y=0, angle=0):
        self.suit = suit # 0 = spades, 1 = clubs, 2 = hearts, 3 = diamonds
        self.value = value # 1 - 9, face cards
        self.owner = owner # who owns this card?

        self.x = x
        self.y = y
        self.angle = angle

        listed_suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
        self.suit_string = listed_suits[self.suit] #  string represent suit in name

        self.image = pygame.image.load(f'images/card{self.suit_string}{str(self.value)}.png')
        # determine card's chance value
        match self.value:
            case 10: # jack
                self.chance = 1
            case 12: # queen
                self.chance = 2
            case 13: # king
                self.chance = 3
            case 14: # ace
                self.chance = 4
            case _: # other cards have no chance value
                self.chance = 0
                

    def __str__(self):
        numbers = ["Zero", "One", "Two", "Three", "Four" , "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
        listed_suits = [['Spades', '♠'], ['Clubs', '♣'], ['Hearts', '♥'], ['Diamonds', '♦']]

        suit_str = listed_suits[self.suit][0] #  string represent suit in name
        suit_art = listed_suits[self.suit][1] #  string represent suit in art

        match self.value:
            case 11:
                return f'J{suit_art} - {numbers[self.value]} of {suit_str}'
            case 12:
                return f'Q{suit_art} - {numbers[self.value]} of {suit_str}'
            case 13:
                return f'K{suit_art} - {numbers[self.value]} of {suit_str}'
            case 14:
                return f'A{suit_art} - {numbers[self.value]} of {suit_str}'
            case _:
                return f'{self.value}{suit_art} - {numbers[self.value]} of {suit_str}'

    
    def __eq__(self, other):
        return self.value == other.value # Card is equal if values are the same

if __name__ == "__main__":
    Game()
