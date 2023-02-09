from cards import Cards


class Poker:
    def __init__(self):
        ...


class Table:

    def __init__(self, cards: Cards = None, ):
        if cards is None:
            self.cards = Cards()
        else:
            self.cards = cards
        self.community_cards = []

    def get_community_cards(self):
        return self.community_cards

    def get_last_card(self):
        return self.cards.cards.pop()
