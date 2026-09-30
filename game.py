from cards import Deck, hand_value, is_blackjack


class Blackjack:
    def __init__(self):
        self.chips = 100

    # ---------- helpers ----------
    def ask(self, prompt):
        """Read input; treat end-of-input (Ctrl+D / Ctrl+Z) as quit."""
        try:
            return input(prompt).strip().lower()
        except EOFError:
            return "q"

    def draw(self, deck):
        """Draw a card; if the deck is ever empty, reshuffle a fresh one."""
        card = deck.draw()
        if card is None:
            print("Deck is empty - reshuffling a new deck.")
            deck.__init__()
            card = deck.draw()
        return card

    def show(self, player, dealer, hide=True):
        if hide:
            shown_dealer = [f"{dealer[0][0]}{dealer[0][1]}", "??"]
        else:
            shown_dealer = [f"{r}{s}" for r, s in dealer]
        print("Dealer:", " ".join(shown_dealer))
        print("Player:", " ".join(f"{r}{s}" for r, s in player),
              "=", hand_value(player))

    def get_wager(self):
        """Ask for a wager. Returns an int, or None if the player quits.
        Invalid input never changes the bankroll."""
        while True:
            raw = self.ask(f"Chips: {self.chips}. Wager (1-{self.chips}) or [q]uit: ")
            if raw == "q":
                return None
            try:
                bet = int(raw)
            except ValueError:
                print("Invalid wager: enter a whole number.")
                continue
            if bet < 1:
                print("Invalid wager: must be at least 1.")
            elif bet > self.chips:
                print(f"Invalid wager: you only have {self.chips} chips.")
            else:
                return bet

    def settle(self, outcome, bet):
        """Apply the result to the bankroll. Called exactly once per round."""
        if outcome == "blackjack":
            delta = bet * 3 // 2
            print(f"Blackjack! You win {delta} chips.")
        elif outcome == "win":
            delta = bet
            print(f"You win {delta} chips.")
        elif outcome == "loss":
            delta = -bet
            print(f"You lose {bet} chips.")
        else:
            delta = 0
            print("Push. Your wager is returned.")
        self.chips += delta

    # ---------- round ----------
    def play_hand(self, deck):
        """Play one hand. Returns 'blackjack', 'win', 'loss', 'push',
        or None if the player quit. Does not touch the bankroll."""
        player = [self.draw(deck), self.draw(deck)]
        dealer = [self.draw(deck), self.draw(deck)]
        self.show(player, dealer)

        # Natural blackjack (21 on the first two cards)
        player_bj = is_blackjack(player)
        dealer_bj = is_blackjack(dealer)
        if player_bj or dealer_bj:
            self.show(player, dealer, hide=False)
            if player_bj and dealer_bj:
                print("Both have blackjack.")
                return "push"
            if player_bj:
                return "blackjack"
            print("Dealer has blackjack.")
            return "loss"

        # Player's turn
        while hand_value(player) < 21:
            key = self.ask("[h]it [s]tand [q]uit: ")
            if key == "q":
                return None
            if key == "s":
                print("You stand.")
                break
            if key == "h":
                card = self.draw(deck)
                player.append(card)
                print(f"You draw {card[0]}{card[1]}.")
                self.show(player, dealer)
            else:
                print("Invalid command. Use h, s or q.")

        if hand_value(player) > 21:
            print("Bust! You went over 21.")
            return "loss"
        if hand_value(player) == 21:
            print("You have 21.")

        # Dealer's turn: hit until 17 or more
        print("Dealer reveals hand.")
        self.show(player, dealer, hide=False)
        while hand_value(dealer) < 17:
            card = self.draw(deck)
            dealer.append(card)
            print(f"Dealer draws {card[0]}{card[1]}.")
            self.show(player, dealer, hide=False)

        pv, dv = hand_value(player), hand_value(dealer)
        if dv > 21:
            print("Dealer busts!")
            return "win"
        if pv > dv:
            return "win"
        if pv < dv:
            return "loss"
        return "push"

    def round(self):
        bet = self.get_wager()
        if bet is None:
            return False
        outcome = self.play_hand(Deck())
        if outcome is None:
            print("Round abandoned. No chips changed.")
            return False
        self.settle(outcome, bet)  # the only place chips change: once per round
        return True

    def run(self):
        print("Blackjack — starting chips:", self.chips)
        while self.chips > 0:
            if not self.round():
                return
            print("Chips:", self.chips)
            if self.chips <= 0:
                print("Out of chips. Game over.")
                return
            if self.ask("Play again? [y/n]: ") != "y":
                return
