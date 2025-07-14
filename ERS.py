import random
def Game():
    num_players= input("How many players?: ")
    main_players_name = input("What is your name?: ")

    deck = [] # initialize the deck of cards for this game
    game_players = [] # Initialize the players playing this game
    '''
    Initialize deck of cards,
    Iterate for each suit to create a new value under that suit,
    Shuffle card objects in deck
    '''
    print(f"\nDeck initializing...(currently {len(deck)} in deck)")
    for suits in range(4):
        for value in range (1,14):
            deck.append(Card(suits, value, -1)) # append this new card to the deck list
    print(f"Deck Initalized! (created {len(deck)} cards in deck)\n")

    print(f"Deck shuffling... (first card = {str(deck[0])})")
    random.shuffle(deck) # shuffle the deck
    print(f"Deck shuffled! (first card now = {str(deck[0])})\n")

    '''
    Create player objects based on desired player count input
    Also randomize names for bots
    Include user + input # of users
    '''
    first_names = ["Zonko", "Fizzler", "Snorple", "Quibly", "Norbix", "Jaxor", "Bloopo", "Zindle", "Crunkle", "Vexon"]
    last_names = ["Glimbo", "Torkel", "Zappy", "Marnix", "Flurbo", "Kazzle", "Droopo", "Wibbit", "Tronix", "Blixel"]
    print("Creating players...")
    game_players.append(Player(0, [], main_players_name)) # Create main player
    for p in range(1, int(num_players) + 0): # Create bot playeres
        game_players.append(Player(p, [], random.choice(first_names)+random.choice(last_names)))
    print("Players created!")
    print("(", end="", flush=True)
    for p in game_players: print(f"{str(p)}, ", end="", flush=True)
    print(")", end="", flush=True)
    
    '''
    Distribute the current game's deck of cards:
    Start with the 0 player --> take the card at index 0 --> append to player's card inventory while removing it from game deck -->
    move to next player --> repeat until no more cards in deck
    '''
    print("\n\nDistributing cards to players...")
    current_player = 0
    while(len(deck) > 0):
        game_players[current_player].inventory.append(deck.pop(0))
        current_player = (current_player + 1) % len(game_players)
    print("Distributed cards to players!")
    for p in game_players: print(f"({str(p)} has {len(p.inventory)} cards.)")

    is_game_won = False
    #is_pattern = False
    current_player = 0

    while not (is_game_won):
        ##check for patterns
        #top_card_index = len(deck) - 1
#
        #if (len(deck) >= 2 and (deck[top_card_index] == deck[top_card_index - 1]) ): # check for pair 
                #is_pattern = True
#
        #if (len(deck) >= 3 and (deck[top_card_index] == deck[top_card_index - 2]) ): # check for sandiwch
                #is_pattern = True

        if(current_player == 0):
            pass
        current_player = (current_player + 1) %  len(game_players)

def player_thread(current_player, player_object):
    
    if (current_player == 0):
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
