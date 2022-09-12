'''Unit Tests for milestone_2.py'''
import unittest
import milestone_2 as m2

class TestPeopleActions(unittest.TestCase):
    '''Tests the public API of the game (player_bet and player_choice)'''
    def setUp(self):
        '''Sets up the necessary objects to play the game'''
        self.player = m2.Player()
        self.dealer = m2.Dealer()
        self.deck = m2.Deck()

    def test_player_bet_errors_on_string(self):
        '''If a player inputs a string to bet, there is an error'''
        self.assertEqual(m2.player_bet(self.player, self.dealer, self.deck, "hi"),
        "Invalid bet. Bet must be an integer")

    def test_player_cant_bet_more_than_stack(self):
        '''If a player bets more than they have, there is an error'''
        self.assertEqual(m2.player_bet(self.player, self.dealer, self.deck,
        m2.player_choice('stack', self.player, self.dealer, self.deck) + 300),
        "Can't bet more than your current stack")

    def test_player_bet_takes_money_away(self):
        '''If a player bets, they have less money after they bet'''
        start = m2.player_choice('stack', self.player, self.dealer, self.deck)
        m2.player_bet(self.player, self.dealer, self.deck, 500)
        end = m2.player_choice('stack', self.player, self.dealer, self.deck)
        self.assertEqual(start - 500, end)

    def test_player_hit_computer_says_hit(self):
        '''If a player hits, the computer tells them they hit'''
        self.assertEqual(m2.player_choice('hit', self.player, self.dealer, self.deck), "Hit!")

if __name__ == "__main__":
    unittest.main()
