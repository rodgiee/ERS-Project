import random
import threading
def Game():
    num_bots= input("How many bots?: ")
    name_player = input("What is your name?: ")

    global deck_game 
    deck_game = [] # initialize the deck_game of cards for this game

    players_game = [] # Initialize the players playing this game
    '''
    Initialize deck_game of cards,
    Iterate for each suit to create a new value under that suit,
    Shuffle card objects in deck_game
    '''
    print(f"\nDeck initializing...(currently {len(deck_game)} in deck_game)")
    for suits in range(4):
        for value in range (1,14):
            deck_game.append(Card(suits, value, -1)) # append this new card to the deck_game list
    print(f"Deck Initalized! (created {len(deck_game)} cards in deck_game)\n")

    print(f"Deck shuffling... (first card = {str(deck_game[0])})")
    random.shuffle(deck_game) # shuffle the deck_game
    print(f"Deck shuffled! (first card now = {str(deck_game[0])})\n")

    '''
    Create player objects based on desired player count input
    Also randomize names for bots
    Include user + input # of users
    '''
    first_names = ["Zonko", "Fizzler", "Snorple", "Quibly", "Norbix", "Jaxor", "Bloopo", "Zindle", "Crunkle", "Vexon"]
    last_names = ["Glimbo", "Torkel", "Zappy", "Marnix", "Flurbo", "Kazzle", "Droopo", "Wibbit", "Tronix", "Blixel"]
    print("Creating players...")
    players_game.append(Player(0, [], name_player)) # Create main player
    for p in range(1, int(num_bots) + 0): # Create bot playeres
        players_game.append(Player(p, [], random.choice(first_names)+random.choice(last_names)))
    print("Players created!")
    print("(", end="", flush=True)
    for p in players_game: print(f"{str(p)}, ", end="", flush=True)
    print(")", end="", flush=True)
    
    '''
    Distribute the current game's deck_game of cards:
    Start with the 0 player --> take the card at index 0 --> append to player's card inventory while removing it from game deck_game -->
    move to next player --> repeat until no more cards in deck_game
    '''
    print("\n\nDistributing cards to players...")
    current_player_id = 0
    while(len(deck_game) > 0):
        players_game[current_player_id].inventory.append(deck_game.pop(0))
        current_player_id = (current_player_id + 1) % len(players_game)
    print("Distributed cards to players!")
    for p in players_game: print(f"({str(p)} has {len(p.inventory)} cards.)")

    is_game_running = True 

    #is_pattern = False
    current_player_id = 0

    # reference to main player object 
    main_player_object = players_game[0]

    global deck_lock
    deck_lock = threading.Lock()

    while (is_game_running):
        main_player = threading.Thread(target=control_player, args=(current_player_id, main_player_object))
        
        ##check for patterns
        #top_card_index = len(deck_game) - 1
#
        #if (len(deck_game) >= 2 and (deck_game[top_card_index] == deck_game[top_card_index - 1]) ): # check for pair 
                #is_pattern = True
#
        #if (len(deck_game) >= 3 and (deck_game[top_card_index] == deck_game[top_card_index - 2]) ): # check for sandiwch
                #is_pattern = True
        
        main_player.start()

        main_player.join()
        current_player_id = (current_player_id + 1) %  len(players_game)
        

def control_player(current_player_id, player_object):
    def slap():
        pass

    def place_card():
        top_card_index = len(player_object.inventory) - 1
        top_card = player_object.inventory.pop(top_card_index)
        deck_lock.acquire()
        deck_game.append(top_card)
        deck_lock.release()

    while(True):
        player_input = input("(p)lace or (s)lap?: ") 
        if (player_input in ['p', 'place']):
            place_card()
            break
        if (player_input in ['s', 'slap']):
            slap()
            break
        
    

    if (current_player_id == 0):
        pass

def bot_thread():
    pass
        
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

    def __str__(self):
        numbers = ["Zero", "One", "Two", "Three", "Four" , "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
        listed_suits = [['Spades', '♠'], ['Clubs', '♣'], ['Hearts', '♥'], ['Diamonds', '♦']]

        suit_str = listed_suits[self.suit][0] #  string represent suit in name
        suit_art = listed_suits[self.suit][1] #  string represent suit in art

        if (self.value == 11): # When card is Jack
            return f'J{suit_art} - {numbers[self.value]} of {suit_str}'

        if (self.value == 12): # When card is Queen
            return f'Q{suit_art} - {numbers[self.value]} of {suit_str}'

        if (self.value == 13): # When card is King
            return f'K{suit_art} - {numbers[self.value]} of {suit_str}'

        if (self.value == 14): # When card is Ace
            return f'A{suit_art} - {numbers[self.value]} of {suit_str}'

        return f'{self.value}{suit_art} - {numbers[self.value]} of {suit_str}'
    
    def __eq__(self, other):
        return self.value == other.value # Card is equal if values are the same

if __name__ == "__main__":
    Game()
