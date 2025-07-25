import pygame
import random
import time
import threading
import os

def game_handler(game_players):
    # game loop main conditional
    # also used by game_visual_handler() to see if game is finished --> closes out if so
    # game_current_player_id checks who's turn is it 
    global is_game_running
    is_game_running = True 
    game_current_player_id = 0

    # mutex lock for game_deck to prevent race conditions
    global deck_lock
    deck_lock = threading.Lock()
    
    # detects if there is either a "sandwich" or "pair", used to check if the player slapped correctly or not
    # used by slap() to verify
    global is_pattern
    is_pattern = False

    # player input needs to be a parallel process, a input_handler always listens for player input and updates to main_player_input
    # whole game loop will hang on player's input if not parallel'
    global main_player_input
    main_player_input = None
    input_thread = threading.Thread(target=input_handler)
    input_thread.start()

    global game_turn_finished

    #clear initalization checks
    time.sleep(1)
    os.system('clear')
    


    # game loop
    while (is_game_running):

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
    
    input_thread.join()

def game_visual_handler():
    pass
def Game():
    '''
    The main body of for ERS game
    It will first:
    1. Initialize shuffle the deck
    2. Create the players 
    3. Distribute out the cards from the deck evenly to the players
    
    
    '''
    game_main_player_name = input("What is your name?: ")
    
    global game_deck 
    game_deck = [] # initialize the game_deck of cards for this game
    game_players = [] # Initialize the players playing this game

    # Initalize the deck with 52 cards and shuffle
    print(f"\nDeck initializing...(currently {len(game_deck)} in game_deck)")
    for suit in range(4):
        for value in range (1,14):
            game_deck.append(Card(suit, value, -1)) # append this new card to the game_deck list
    print(f"Deck Initalized! (created {len(game_deck)} cards in game_deck)\n")

    print(f"Deck shuffling... (first card = {str(game_deck[0])})")
    random.shuffle(game_deck) # shuffle the game_deck
    print(f"Deck shuffled! (first card now = {str(game_deck[0])})\n")

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
    for game_player in game_players: print(f"{str(game_player)}, ", end="", flush=True)
    print(")", end="", flush=True)
    
    # Distribute the game deck of 52 cards evenly to all players
    print("\n\nDistributing cards to players...")
    game_current_player_id = 0
    while(len(game_deck) > 0):
        game_players[game_current_player_id].inventory.append(game_deck.pop(0))
        game_current_player_id = (game_current_player_id + 1) % len(game_players)
    print("Distributed cards to players!")
    for p in game_players: print(f"({str(p)} has {len(p.inventory)} cards.)")

    game_thread = threading.Thread(target=game_handler, args=(game_players))
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

    global is_game_running

    while(is_game_running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_running = False

        game_background_color = '0x80001f'
        game_screen.fill(game_background_color)

        for surface in surface_load:
            pygame.draw.rect(game_screen, surface[0], surface[1])
        pygame.display.flip()

    game_thread.join()





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
        player_object.inventory.extend(game_deck)
        game_deck = []

def place_card(player_object):
    # take the card from player's inventory at the last index and append to game deck
    top_card_index = len(player_object.inventory) - 1
    top_card = player_object.inventory.pop(top_card_index)
    
    deck_lock.acquire()
    game_deck.append(top_card)
    check_pattern()
    deck_lock.release()
    
    print(f'{str(player_object)} places {top_card}')

    return top_card

def input_handler():
    global main_player_input
    while(True):
        main_player_input = str(input())

def control_player(game_current_player_id, player_object, player_id):
    global game_turn_finished
    if (player_id == 0): # case if main player
        while(not game_turn_finished):
            global main_player_input
            if (main_player_input in ['p', 'place'] and game_current_player_id == player_id):
                place_card(player_object)
                main_player_input = None
                break
            if (main_player_input in ['s', 'slap']):
                slap(player_object)
                main_player_input = None
                break
    else: # case if bot
        if game_current_player_id == player_id:
            time.sleep(random.random() * 2 ) 
            place_card(player_object)
            game_turn_finished = True
            return
    return

class Player:
    '''
    Player = id, card inventory, name
    '''
    def __init__(self, p_id, name, position, inventory = []):
        self.p_id = p_id # integer player identifier
        self.inventory = inventory # list of cards player holds
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
    def __init__(self, suit, value, owner):
        self.suit = suit # 0 = spades, 1 = clubs, 2 = hearts, 3 = diamonds
        self.value = value # 1 - 9, face cards
        self.owner = owner # who owns this card?
        
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
