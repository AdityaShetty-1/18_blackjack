import random

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

SUITS = ["C", "D", "H", "S"]


class Deck:
    def __init__(self):
        self.cards = [(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None


def hand_value(hand):
    total = 0
    aces = 0
    for rank, _ in hand:
        if rank == "A":
            total += 11
            aces += 1
        elif rank in {"J", "Q", "K"}:
            total += 10
        else:
            total += int(rank)
    # Downgrade Aces from 11 to 1 one at a time while the hand is bust
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def is_blackjack(hand):
    return len(hand) == 2 and hand_value(hand) == 21
