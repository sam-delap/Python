import random
from os import system
def print_rules():
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
    def __init__(self):
        self.hand = []
        self.aces = 0

    def hit(self, deck):
        card = deck.deal()
        self.hand.append(card)
        if(check_card_value(card) == 11):
            self.aces += 1
        return "Hit!"

class Dealer(Person):
    def __init__(self):
        super().__init__()
        self.show = False

class Player(Person):
    def __init__(self):
        super().__init__()
        self.stack = 1000
        self.stand = False
        self.bet = 0

    def reset(self):
        self.hand = []
        self.aces = 0
        self.bet = 0

class Deck():
    def __init__(self):
        self.cards = [x for x in range(52)]
    
    def deal(self):
        random.shuffle(self.cards)
        card = self.cards.pop()
        return card

    def __len__(self):
        return len(self.cards)

def player_bet(player, dealer, deck, bet):
    try:
        bet = int(bet)
    except ValueError:
        return "Invalid bet"
    else:
        player.stack -= bet
        player.bet += bet
        player.hit(deck)
        player.hit(deck)
        dealer.hit(deck)
        dealer.hit(deck)
        return "Bet placed"

def player_choice(choice, player, dealer=Dealer(), deck=[1,2]):
    if choice == 'hit':
        return player.hit(deck)
    elif choice == 'stand':
        return player_stand(player, dealer, deck)
    elif choice == 'stack':
        return player.stack
    else:
        return -1

def check_hand_value(person):
    val = sum([check_card_value(card) for card in person.hand])
    if type(person) == Dealer and person.show == False:
        return check_card_value(person.hand[0])
    else:
        if person.aces > 0 and val > 21:
            val -= 10 * person.aces
        return val

def check_card_suit(card):
    switcher = {
        0: "H",
        1: "D",
        2: "C",
        3: "S"
    }

    return switcher[card // 13]

def player_stand(player, dealer, deck):
    player.stand = True
    dealer.show = True
    handle_dealer_hand(dealer, deck)
    return "Stand!"

def check_player_win(player, dealer):
    player_hand_val = check_hand_value(player)
    dealer_hand_val = check_hand_value(dealer)

    if player_hand_val < dealer_hand_val and dealer_hand_val <= 21 and dealer.show:
        return "You failed to beat the dealer. Better luck next time!"
    elif player_hand_val == 21:
        player.stack += player.bet * 1.5
        return "You hit 21. Congratulations!"
    elif player_hand_val >= dealer_hand_val and player_hand_val < 21 and dealer.show:
        player.stack += player.bet * 2
        return "You beat the dealer. Congratulations!"
    elif player_hand_val > 21:
        return "Player busts! Better luck next time!"
    elif dealer_hand_val > 21:
        player.stack += player.bet * 2
        return "Dealer busts! Congratulations!"
    else:
        return "\n"

def show_hand(person):
    hand = ""
    if type(person) == Dealer and not person.show:
        hand += f"{check_card_symbol(person.hand[0])}{check_card_suit(person.hand[0])} ?"
    else:
        for card in person.hand:
            hand += f"{check_card_symbol(card)}{check_card_suit(card)} "
    return hand

def check_card_value(card):
    value = card % 13 + 2
    if value <= 10:
        return value
    elif value != 14:
        return 10
    else:
        return 11

def handle_dealer_hand(dealer, deck):
    while check_hand_value(dealer) < 17:
        dealer.hit(deck)
        show_hand(dealer)

def check_card_symbol(card):
    value = card % 13 + 2
    switcher = {
        11: "J",
        12: "Q",
        13: "K",
        14: "A"
    }

    if value <= 10:
        return str(value)
    else:
        return switcher[value]

def player_place_bet(player, dealer, deck):
    print(f"Your stack size is: {player.stack}")
    bet = input("Place your bet: ")
    msg = player_bet(player, dealer, deck, bet)
    system('clear')
    print(msg)
    return msg

def player_make_choice(player, dealer, deck):
    print("What would you like to do?", sep="")
    choice = input("(hit, stand, stack):  ")
    msg = player_choice(choice, player, dealer, deck)
    print(msg)
    return msg

def print_hands(player, dealer):
    print(f"Player hand: {show_hand(player)} ({check_hand_value(player)})")
    print(f"Dealer hand: {show_hand(dealer)} ({check_hand_value(dealer)})")    

if __name__ == "__main__":
    print_rules()
    player = Player()

    # While the player still has chips
    while(player.stack > 0):
        dealer = Dealer()
        deck = Deck()
        while player_place_bet(player, dealer, deck) == "Invalid bet":
            player_place_bet(player, dealer, deck)

        system('clear')
        print_hands(player, dealer)

        while player_make_choice(player, dealer, deck) != "Stand!" and check_player_win(player, dealer) == "\n":
            print_hands(player, dealer)

        dealer.show = True
        print_hands(player, dealer)
        print(check_player_win(player, dealer))

        player.reset()