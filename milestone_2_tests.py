import unittest
import milestone_2 as m2

class TestPeopleActions(unittest.TestCase):
    def setUp(self):
        self.player = m2.Player()
        self.dealer = m2.Dealer()
        self.deck = m2.Deck()

    def test_player_bet_errors_on_string(self):
        self.assertEqual(m2.player_bet(self.player, self.dealer, self.deck, "hi"), "Invalid bet")

    def test_player_bet_takes_money_away(self):
        start = m2.player_choice('stack', self.player, self.dealer, self.deck)
        m2.player_bet(self.player, self.dealer, self.deck, 500)
        end = m2.player_choice('stack', self.player, self.dealer, self.deck)
        self.assertEqual(start - 500, end)

    def test_dealer_shows_one_card_before_stand(self):
        m2.player_bet(self.player, self.dealer, self.deck, 500)
        value = m2.dealer_show_hand(self.dealer)
        self.assertIn("?", value)

    def test_dealer_shows_both_cards_after_stand(self):
        m2.player_bet(self.player, self.dealer, self.deck, 500)
        m2.player_choice('stand', self.player, self.dealer, self.deck)
        value = m2.dealer_show_hand(self.dealer)
        self.assertNotIn("?", value)

    def test_after_player_stand_dealer_hand_value_more_than_17(self):
        m2.player_bet(self.player, self.dealer, self.deck, 500)
        m2.player_choice('stand', self.player, self.dealer, self.deck)
        self.assertGreaterEqual(m2.check_hand_value(self.dealer), 17)

if __name__ == "__main__":
    unittest.main()