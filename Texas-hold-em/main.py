class Card:
    suit = 'A'
    rank = 0

    def __init__(self, card):
        self.suit = card[0]
        card = card[1:]
        if card == "2": self.rank = 2
        elif card == "3": self.rank = 3
        elif card == "4": self.rank = 4
        elif card == "5": self.rank = 5
        elif card == "6": self.rank = 6
        elif card == "7": self.rank = 7
        elif card == "8": self.rank = 8
        elif card == "9": self.rank = 9
        elif card == "10": self.rank = 10
        elif card == "J": self.rank = 11
        elif card == "Q": self.rank = 12
        elif card == "K": self.rank = 13
        elif card == "A": self.rank = 14

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.suit

    def __gt__(self, other):
        return self.rank > other.rank

class Poker_hand:
    cards = []
    poker_hand = 0 #1:high card 2:one pair 3:two pair 4:three of a kind 5:straight 6:flush 7:full house 8:four of a kind 9:straight flush
    strength = []

    def __init__(self, card_list):
        card_list.sort(reverse=True)
        self.cards = card_list
        self.poker_hand, self.strength = self.hand()

    def __lt__(self, other):
        if self.poker_hand < other.poker_hand: return True
        if self.poker_hand > other.poker_hand: return False
        if self.poker_hand == 5 or self.poker_hand == 9:
            return self.strength[0] < other.strength[0]
        if self.poker_hand == 7 or self.poker_hand == 8:
            return self.strength[0] < other.strength[0] or (self.strength[0] == other.strength[0] and self.strength[1] < other.strength[1])
        if self.poker_hand == 3 or self.poker_hand == 4:
            for i in range(3):
                if self.strength[i] < other.strength[i]: return True
                if self.strength[i] > other.strength[i]: return False
            return False
        if self.poker_hand == 2:
            for i in range(4):
                if self.strength[i] < other.strength[i]: return True
                if self.strength[i] > other.strength[i]: return False
            return False
        for i in range(5):
                if self.strength[i] < other.strength[i]: return True
                if self.strength[i] > other.strength[i]: return False
        return False

    def hand(self):
        flush = (False, '')
        straight = (False, 0)
        count_same_rank = 1
        count_consecutive_rank = 1
        pairs = []
        triples = []
        quadraple = 0
        count_suits = {'H': 0, 'D': 0, 'S': 0, 'C': 0}

        count_suits[self.cards[0].suit] += 1

        for i in range(1, 7):
            count_suits[self.cards[i].suit] += 1
            if self.cards[i].rank == self.cards[i-1].rank:
                count_same_rank += 1
            else:
                if count_same_rank == 2:
                    pairs.append(self.cards[i-1].rank)
                elif count_same_rank == 3:
                    triples.append(self.cards[i-1].rank)
                elif count_same_rank == 4:
                    quadraple = self.cards[i-1].rank
                count_same_rank = 1
                if self.cards[i].rank == self.cards[i-1].rank - 1:
                    count_consecutive_rank += 1
                    if count_consecutive_rank == 5:
                        straight = (True, self.cards[i].rank + 4)
                else:
                    count_consecutive_rank = 1

        if count_same_rank == 2:
            pairs.append(self.cards[6].rank)
        if count_same_rank == 3:
            triples.append(self.cards[6].rank)
        if count_same_rank == 4:
            quadraple = self.cards[6].rank

        if count_consecutive_rank == 4 and self.cards[0].rank - self.cards[6].rank == 12:
            straight = (True, 5)

        if count_suits['H'] >= 5:
            flush = (True, 'H')
        elif count_suits['D'] >= 5:
            flush = (True, 'D')
        elif count_suits['S'] >= 5:
            flush = (True, 'S')
        elif count_suits['C'] >= 5:
            flush = (True, 'C')

        if straight[0] and flush[0]:
            has_Ace = False
            rank = 0
            count_consecutive_rank = 1
            for i in range(7):
                if self.cards[i].suit == flush[1]:
                    if rank == 0:
                        rank = self.cards[i].rank
                        if rank == 14:
                            has_Ace = True
                    elif self.cards[i].rank == rank-1:
                        count_consecutive_rank += 1
                        if count_consecutive_rank == 5:
                            return 9, [rank + 3]
                        rank -= 1
                    else:
                        count_consecutive_rank = 1
                        rank = self.cards[i].rank
            if has_Ace and rank == 2 and count_consecutive_rank == 4:
                return 9, [5]

        if quadraple:
            for i in range(7):
                if self.cards[i].rank != quadraple:
                    return 8, [quadraple, self.cards[i].rank]

        if len(triples) == 2:
            return 7, triples

        if len(triples) and len(pairs):
            return 7, triples + [pairs[0]]

        if flush[0]:
            ranks = []
            for i in range(7):
                if self.cards[i].suit == flush[1]:
                    ranks.append(self.cards[i].rank)
                    if len(ranks) == 5:
                        return 6, ranks

        if straight[0]:
            return 5, [straight[1]]

        if len(triples) == 1:
            ranks = []
            for i in range(7):
                if self.cards[i].rank != triples[0]:
                    ranks.append(self.cards[i].rank)
                    if len(ranks) == 2:
                        return 4, triples + ranks

        if len(pairs) >= 2:
            for i in range(7):
                if self.cards[i].rank != pairs[0] and self.cards[i].rank != pairs[1]:
                    return 3, [pairs[0], pairs[1], self.cards[i].rank]

        if len(pairs) == 1:
            ranks = []
            for i in range(7):
                if self.cards[i].rank != pairs[0]:
                    ranks.append(self.cards[i].rank)
                    if len(ranks) == 3:
                        return 2, pairs + ranks

        return 1, [self.cards[0].rank, self.cards[1].rank, self.cards[2].rank, self.cards[3].rank, self.cards[4].rank]

    def print_hand(self):
        if self.poker_hand == 1:
            print("High card")
        if self.poker_hand == 2:
            print("One pair")
        if self.poker_hand == 3:
            print("Two pair")
        if self.poker_hand == 4:
            print("Three of a kind")
        if self.poker_hand == 5:
            print("Straight")
        if self.poker_hand == 6:
            print("Flush")
        if self.poker_hand == 7:
            print("Full house")
        if self.poker_hand == 8:
            print("Four of a kind")
        if self.poker_hand == 9:
            print("Stright flush")

yours = input("개인 패 2장을 입력하세요. ").split()
your_hand = []
for i in range(2):
    your_hand.append(Card(yours[i]))

opponent = input("상대의 패 2장을 입력하세요. ").split()
opponent_hand = []
for i in range(2):
    opponent_hand.append(Card(opponent[i]))

community = input("공유 카드를 입력하세요. ").split()
community_cards = []
for i in range(5):
    community_cards.append(Card(community[i]))

h1 = Poker_hand(your_hand + community_cards)
h2 = Poker_hand(opponent_hand + community_cards)

h1.print_hand()
h2.print_hand()

if h1 < h2:
    print("Lose")
elif h1 > h2:
    print("Win")
else:
    print("Draw")