import random
def Game(num_players):
    deck = [] # initialize the deck of cards for this game
    game_players = [] # Initialize the players playing this game
    '''
    Initialize deck of cards, a nested loop where each suit will be iterated for all possible values in cards
    '''
    for suits in range(4):
        for value in range (1,14):
            deck.append(Card(suits, value, -1)) # append this new card to the deck list

    random.shuffle(deck) # shuffle the deck

    for p in range(1, int(num_players) + 1):
        game_players.append(Player(p, []))

    current_player = 0
    while(len(deck) > 0):
        game_players[current_player].player_cards.append(deck.pop(0))
        current_player = (current_player + 1) % 3

    breakpoint()
class Player:
    def __init__(self, player_id, player_cards):
        self.player_id = player_id # integer player identifier
        self.player_cards = player_cards # list of cards player holds

class Card:
    def __init__(self, suit, value, owner):
        self.suit = suit # 0 = spades, 1 = clubs, 2 = hearts, 3 = diamonds
        self.value = value # 1 - 9, face cards
        self.owner = owner # who owns this card?

    def __str__(self):
        numbers = ["Zero", "One", "Two", "Three", "Four" , "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
        listed_suits = [['Spades', '♠'], ['Clubs', '♣'], ['Hearts', '♥'], ['Diamonds', '♦']]
        suit_str = listed_suits[self.suit][0] # clubs, spades, hearts, diamonds
        suit_art = listed_suits[self.suit][1] # clubs, spades, hearts, diamonds
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
        return self.value == other.value

if __name__ == "__main__":
    input_players = input("How many players?: ")
    Game(input_players)
