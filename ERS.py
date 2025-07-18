import random
import time
import threading
import os

def Game():
    game_bot_count= input("How many bots?: ")
    game_main_player_name = input("What is your name?: ")
    
    global game_deck 
    game_deck = [] # initialize the game_deck of cards for this game

    game_players = [] # Initialize the players playing this game
    '''
    Initialize game_deck of cards,
    Iterate for each suit to create a new value under that suit,
    Shuffle card objects in game_deck
    '''
    print(f"\nDeck initializing...(currently {len(game_deck)} in game_deck)")
    for suit in range(4):
        for value in range (1,14):
            game_deck.append(Card(suit, value, -1)) # append this new card to the game_deck list
    print(f"Deck Initalized! (created {len(game_deck)} cards in game_deck)\n")

    print(f"Deck shuffling... (first card = {str(game_deck[0])})")
    random.shuffle(game_deck) # shuffle the game_deck
    print(f"Deck shuffled! (first card now = {str(game_deck[0])})\n")

    '''
    Create player objects based on desired player count input
    Also randomize names for bots
    Include user + input # of users
    '''
    random_first_names = ["Zonko", "Fizzler", "Snorple", "Quibly", "Norbix", "Jaxor", "Bloopo", "Zindle", "Crunkle", "Vexon"]
    random_last_names = ["Glimbo", "Torkel", "Zappy", "Marnix", "Flurbo", "Kazzle", "Droopo", "Wibbit", "Tronix", "Blixel"]
    print("Creating players...")
    game_players.append(Player(0, [], game_main_player_name)) # Create main player
    for player_index in range(1, int(game_bot_count) + 1): # Create bot playeres
        game_players.append(Player(player_index, [], random.choice(random_first_names)+random.choice(random_last_names)))
    print("Players created!")
    print("(", end="", flush=True)
    for game_player in game_players: print(f"{str(game_player)}, ", end="", flush=True)
    print(")", end="", flush=True)
    
    '''
    Distribute the current game's game_deck of cards:
    Start with the 0 player --> take the card at index 0 --> append to player's card inventory while removing it from game game_deck -->
    move to next player --> repeat until no more cards in game_deck
    '''
    print("\n\nDistributing cards to players...")
    game_current_player_id = 0
    while(len(game_deck) > 0):
        game_players[game_current_player_id].inventory.append(game_deck.pop(0))
        game_current_player_id = (game_current_player_id + 1) % len(game_players)
    print("Distributed cards to players!")
    for p in game_players: print(f"({str(p)} has {len(p.inventory)} cards.)")

    is_game_running = True 

    #is_pattern = False
    game_current_player_id = 0

    # reference to main player object 
    main_player_object = game_players[0]

    global deck_lock
    deck_lock = threading.Lock()
    
    global is_pattern
    is_pattern = False
    time.sleep(3)
    os.system('clear')
    while (is_game_running):
        game_main_player = threading.Thread(target=control_player, args=(game_current_player_id, main_player_object, 0))
        bot_threads = []
        for bot_index in range(1, len(game_players)):
            bot_threads.append(threading.Thread(target=control_player, args=(game_current_player_id, game_players[bot_index], bot_index)))

        game_main_player.start()
        for bot in bot_threads:
            bot.start()
        
        game_main_player.join()
        for bot in bot_threads:
            bot.join()
               
        game_current_player_id = (game_current_player_id + 1) %  len(game_players)

def check_pattern():
    top_card_index = len(game_deck) - 1
    global is_pattern
    if (len(game_deck) >= 2 and (game_deck[top_card_index] == game_deck[top_card_index - 1]) ): # check for pair 
        is_pattern = True
    elif (len(game_deck) >= 3 and (game_deck[top_card_index] == game_deck[top_card_index - 2]) ): # check for sandwich
        is_pattern = True
    else:
        is_pattern = False

def slap():
    pass

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

def control_player(game_current_player_id, player_object, player_id):
    if (player_id == 0 and game_current_player_id == player_id): # case if main player
        while(True):
            player_input = input("(p)lace or (s)lap?: ") 
            if (player_input in ['p', 'place']):
                place_card(player_object)
                break
            if (player_input in ['s', 'slap']):
                slap()
                break
    else: # case if bot
        if game_current_player_id == player_id:
            time.sleep(random.random() * 2) 
            place_card(player_object)
            return

class Player:
    '''
    Player = id, card inventory, name
    '''
    def __init__(self, p_id, inventory, name):
        self.p_id = p_id # integer player identifier
        self.inventory = inventory # list of cards player holds
        self.name = name # string name of player
    
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
