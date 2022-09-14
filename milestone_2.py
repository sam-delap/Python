'''This module is a beginner OOP version of Blackjack that implements TDD and pylint'''
import random
from os import system

def print_rules():
    '''Print the rules of Blackjack'''
    rules_list = ["You bet at the start of each round",
    "You may bet any amount between $2 and $500",
    "Each round, you are given 2 cards to start with",
    "You can \'hit\' to add more cards to your total",
    "Your goal is to beat the dealer by getting as close to 21 as possible, without going over",
    "However, you will only know one of the dealer's cards",
    "If you go over 21, you will \'bust\' and lose your bet",
    "If you don't want to add cards to your hand, you can \'stand\' to stop receiving cards",
    "Once you \'stand\' or \'bust\', the dealer will reveal his other card",
    "The dealer will then \'hit\' until their hand is over 17",
    "If you hit 21 exactly, you receive 1.5x your bet",
    "If the dealer busts or fails to beat your hand, you receive 2x your bet",
    "If you fail to beat the dealer, you lose your bet"]
    print("Welcome to Blackjack!\nHere's how to play:\n" + "\n".join(rules_list))
class Person():
    '''The parent class of the dealer and player. Contains information about the hand.'''
    def __init__(self):
        self.hand = []
        self.aces = 0

    def hit(self, deck):
        '''Add a card to the person's hand'''
        card = deck.deal()
        self.hand.append(card)
        if check_card_value(card) == 11:
            self.aces += 1
        return "Hit!"

    def show_hand(self):
        '''Display a formatted version of the person's hand'''
        hand = ""
        for card in self.hand:
            hand += f"{check_card_symbol(card)}{check_card_suit(card)} "
        return hand

    def hand_value(self):
        '''Check the value of a person's hand'''
        val = sum([check_card_value(card) for card in self.hand])
        if self.aces > 0 and val > 21:
            val -= 10 * self.aces
        return val

class Dealer(Person):
    '''The dealer of the table. Typically only one'''
    def __init__(self):
        super().__init__()
        self.show = False

    def hand_value(self):
        '''Check the value of the dealer's hand'''
        if self.show:
            return super().hand_value()
        return check_card_value(self.hand[0])

    def show_hand(self):
        '''Display a formatted version of the dealer's hand'''
        if self.show:
            super().show_hand()
        return f"{check_card_symbol(self.hand[0])}{check_card_suit(self.hand[0])} ?"

    def deal_hand(self, deck):
        '''Handle the dealer's hand after the player stands'''
        self.show = True
        while self.hand_value() < 17:
            card = deck.deal()
            self.hand.append(card)

class Player(Person):
    '''The player(s) at the table'''
    def __init__(self):
        super().__init__()
        self.stack = 1000
        self.bet = 0
        self.play = True

    def reset(self):
        '''Get the player ready for a new round of play'''
        self.hand = []
        self.aces = 0
        self.bet = 0

class Deck():
    '''The deck. Represented by 52 cards.'''
    def __init__(self):
        self.cards = list(range(52))

    def deal(self):
        '''Take a random card from the deck, without replacement'''
        random.shuffle(self.cards)
        card = self.cards.pop()
        return card

    def __len__(self):
        return len(self.cards)

def player_bet(player, dealer, deck, bet):
    '''Handles player betting and initial dealing of hands'''
    try:
        bet = int(bet)
        if bet > player.stack:
            return "Can't bet more than your current stack"
    except ValueError:
        return "Invalid bet. Bet must be an integer"
    else:
        player.stack -= bet
        player.bet += bet
        player.hit(deck)
        player.hit(deck)
        dealer.hit(deck)
        dealer.hit(deck)
        return "Bet placed"

def player_choice(choice, player, dealer=Dealer(), deck=Deck()):
    '''Handles player decisions'''
    if choice == 'hit':
        return player.hit(deck)
    if choice == 'stand':
        dealer.deal_hand(deck)
        return "Stand!"
    if choice == 'stack':
        return player.stack
    return "Invalid choice"

def check_card_suit(card):
    '''Checks the suit of a given card'''
    switcher = {
        0: "H",
        1: "D",
        2: "C",
        3: "S"
    }

    return switcher[card // 13]

def check_player_win(player, dealer):
    '''Checks the outcome of a hand'''
    player_hand_val = player.hand_value()
    dealer_hand_val = dealer.hand_value()

    if player_hand_val < dealer_hand_val <= 21 and dealer.show:
        return "You failed to beat the dealer. Better luck next time!"
    if player_hand_val == 21:
        player.stack += player.bet * 1.5
        return "You hit 21. Congratulations!"
    if dealer_hand_val <= player_hand_val < 21 and dealer.show:
        player.stack += player.bet * 2
        return "You beat the dealer. Congratulations!"
    if player_hand_val > 21:
        return "Player busts! Better luck next time!"
    if dealer_hand_val > 21:
        player.stack += player.bet * 2
        return "Dealer busts! Congratulations!"
    return "\n"

def check_card_value(card):
    '''Checks the value of a card according to the rules of blackjack'''
    value = card % 13 + 2
    if value <= 10:
        return value

    if value != 14:
        return 10

    return 11

def check_card_symbol(card):
    '''Checks the symbol of a card'''
    value = card % 13 + 2
    switcher = {
        11: "J",
        12: "Q",
        13: "K",
        14: "A"
    }

    if value <= 10:
        return str(value)

    return switcher[value]

def player_place_bet(player, dealer, deck):
    '''Handles the prompt for player betting'''
    print(f"Your stack size is: {player.stack}")
    bet = input("Place your bet: ")
    msg = player_bet(player, dealer, deck, bet)
    system('clear')
    print(msg)
    return msg

def player_make_choice(player, dealer, deck):
    '''Handles the prompt for player choice'''
    print("What would you like to do?", sep="")
    choice = input("(hit, stand, stack):  ")
    msg = player_choice(choice, player, dealer, deck)
    print(msg)
    return msg

def print_hands(player, dealer):
    '''Prints the player(s) and dealer's hands in a formatted way'''
    print(f"Player hand: {player.show_hand()} ({player.hand_value()})")
    print(f"Dealer hand: {dealer.show_hand()} ({dealer.hand_value()})")

if __name__ == "__main__":
    print_rules()
    my_player = Player()

    # While the player still has chips and wants to play
    while(my_player.stack > 0 and my_player.play):
        my_dealer = Dealer()
        my_deck = Deck()
        while player_place_bet(my_player, my_dealer, my_deck) == "Invalid bet":
            player_place_bet(my_player, my_dealer, my_deck)

        system('clear')
        print_hands(my_player, my_dealer)

        while player_make_choice(my_player, my_dealer, my_deck) != "Stand!" \
            and check_player_win(my_player, my_dealer) == "\n":
            print_hands(my_player, my_dealer)

        my_dealer.show = True
        print_hands(my_player, my_dealer)
        print(check_player_win(my_player, my_dealer))

        my_player.reset()

    print("Thanks for playing!")
