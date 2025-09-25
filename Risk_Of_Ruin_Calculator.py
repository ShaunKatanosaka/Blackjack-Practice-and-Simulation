'''
risk of ruin calculator
	simulation
	house edge calculator
app for practice
	counting
	book optimal/illustrious 18
settings:
set cut card location
show/hide current count

'''

"""
general plan:

blackjack optimal play simulator
simulate betting strategy
monte cristo simulation for calculating house edge/risk of ruin


function for optimal play
"""


from typing import final
from msilib import datasizemask
from operator import truediv
from pickle import TRUE
import random
import pandas as pd

hard_totals = pd.read_csv("D:\Visual Studio Files\Blackjack Projects\Risk Of Ruin Calculator\hard totals.csv")
soft_totals= pd.read_csv("D:\Visual Studio Files\Blackjack Projects\Risk Of Ruin Calculator\soft totals.csv")
splits = pd.read_csv("D:\Visual Studio Files\Blackjack Projects\Risk Of Ruin Calculator\splits.csv")
splitDict = {"A" : 0,
             "K" : 1,
             "Q" : 1,
             "J" : 1,
             "10":1,
             "9" :2,
             "8":3,
             "7":4,
             "6":5,
             "5":6,
             "4":7,
             "3":8,
             "2":9
}


suit_symbols = {
    'S': '♠',
    'H': '♥',
    'D': '♦',
    'C': '♣'
}
class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = self.get_value()

    def __str__(self):
        return str(self.rank + suit_symbols[self.suit])

    def get_value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 1  # handle later as 1 or 11
        else:
            return int(self.rank)

class Deck:
    def __init__(self, num_decks=6):
        self.cards = self.build_deck(num_decks)
        random.shuffle(self.cards)

    def get_cards_left(self):
        return len(self.cards)

    def build_deck(self, num_decks):
        ranks = [str(n) for n in range(2,11)] + ['J','Q','K','A']
        suits = ['H','D','C','S']
        return [Card(rank, suit) for rank in ranks for suit in suits] * num_decks

    def deal_card(self):
        #if len(self.cards) < 60:  # penetration threshold
        #    self.__init__()
        return self.cards.pop()

    def print_cards(self):
        CardsLeftStr = {}
        for card in self.cards:
            cardStr = str(card)
            if cardStr in CardsLeftStr:
                CardsLeftStr[cardStr] += 1
            else:
                CardsLeftStr[cardStr] = 1
        print(dict(sorted(CardsLeftStr.items())))

    def get_count(self):
        count = 0
        for card in self.cards:
            if 2 <= card.value <= 6:
                count += 1
            elif 7 <= card.value <= 9:
                count += 0
            elif card.value == 10 or card.rank == "A":
                count -= 1
            else:
                print("wtf")
        return 0 - count

    def print_count(self):
        if self.get_count() > 0:
            print("+{0}".format(self.get_count()))
        else:
            print(self.get_count())

class Hand:
    def __init__(self, input_bet = 25):
        self.cards = []
        self.softTotal = False
        self.bet = input_bet
        self.betMultiplier = 1
    def add_card(self, card):
        self.cards.append(card)
    def clear_hand(self):
        self.cards = []

    def contains_ace(self):
        containsAce = False
        for card in self.cards:
            if card.rank == 'A':
                containsAce = True
            break
        return containsAce

    def get_values(self):
        total = sum(card.value for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == 'A')
        if total <= 11 and aces:
            self.softTotal = True
            total += 10
        else:
            self.softTotal = False
        return total

    def print_values(self):
        print(self.get_values())

    def display_hand(self):
        handList = []
        for card in self.cards:
            handList.append(str(card))
        print(handList)

    def display_one_hand(self):
        print(str(self.cards[0]))



class GameSimulator:
    def __init__(self, num_decks=2, autoPlay_input = False, bankroll=1000, cut_card_spot = 0.75):
        self.numberOfDecks = num_decks
        self.deck = Deck(self.numberOfDecks)
        self.bankroll = bankroll
        self.initial_bankroll = bankroll
        self.cut_card_spot = cut_card_spot
        self.bankroll_progress = []
        self.total_wagered = 0
        # hit 17 game
        self.displayMode = True
        self.hands_played = 0
        self.number_of_players = 1
        self.initial_number_of_players = self.number_of_players
        self.autoPlay = autoPlay_input
        self.shoes_played = 1
        self.hands_played_in_shoe = 0

    def display_hands(self, players, dealer):
        if self.displayMode:
            dealer.display_one_hand()
            print("\n")
            for i in range(self.number_of_players):
                players[i].display_hand()
                players[i].print_values()
            #print("\n")
    
    def display_all_hands(self, players, dealer):
        if self.displayMode:
            dealer.display_hand()
            dealer.print_values()
            print("\n")
            for i in range(self.number_of_players):
                players[i].display_hand()
                players[i].print_values()
            #print("\n")

    def play_hand(self, bet_input = 25):
        cardsCut = self.cut_card_spot * 52 * self.numberOfDecks
        # bet strategy
        # insert rules as parameter?
        bet = bet_input
        players = []
        for i in range(self.number_of_players):
            players.append(Hand(bet))
        dealer = Hand()

        self.hands_played += 1

        if self.deck.get_cards_left() <= cardsCut:
           self.deck = Deck(self.numberOfDecks)
           self.shoes_played += 1
           self.hands_played_in_shoe = 0
           if self.displayMode:
               print("new shoe")

        #deal cards
        if self.deck.get_cards_left() > cardsCut:
            for i in range(self.number_of_players):
               #first player card
               players[i].add_card(self.deck.deal_card())
               #(test with specific card)  
               #players[i].add_card(Card("A","H"))
               
            dealer.add_card(self.deck.deal_card())
            #(test with specific card)   dealer.add_card(Card("6","H"))
            for i in range(self.number_of_players):
                #second player card
                players[i].add_card(self.deck.deal_card())
                #(test with specific card) 
                #players[i].add_card(Card("A","H"))
            dealer.add_card(self.deck.deal_card())
            self.hands_played_in_shoe += 1

        hands_total = self.number_of_players
        dealer_blackjack = False
        i = 0
        while i < hands_total:
            hand_over = False
            if dealer.get_values() == 21:
                hand_over = True
                if self.displayMode:
                   print("dealer blackjack")
                dealer_blackjack = True

            if players[i].get_values() == 21:
                hand_over = True
                if self.displayMode:
                   print("player blackjack")
                if not dealer_blackjack:
                    players[i].betMultiplier = 1.5

            if len(players[i].cards) == 1:
                players[i].add_card(self.deck.deal_card())
            if  self.displayMode:
                if hand_over:
                    self.display_all_hands(players, dealer)
                else:
                    self.display_hands(players,dealer)
                print("wager: ${0}".format(players[i].bet))
            while(not hand_over):
                x = ''
                if not self.autoPlay:
                    x = input();
                else:
                    players[i].get_values() #to update softTotal
                    dealerUpcard = dealer.cards[0].rank
                    if dealerUpcard == "J" or dealerUpcard == "Q" or dealerUpcard == "K":
                        dealerUpcard = "10"
                    if players[i].cards[0].value == players[i].cards[1].value and len(players[i].cards) == 2:
                        # splits
                        YorN = splits[dealerUpcard][splitDict[players[i].cards[0].rank]]
                        if YorN == "Y":
                            assert len(players[i].cards) == 2, "player does not have 2 cards"
                            assert players[i].cards[0].value == players[i].cards[1].value
                            x = 'p'
                        
                    if players[i].softTotal and x == '':
                        #soft totals
                        if players[i].get_values() == 21:
                            x = 's'
                        else:
                            x = soft_totals[dealerUpcard][20-players[i].get_values()]

                    elif x == '':
                        #hard total
                        if 17 <= players[i].get_values() <= 21:
                            x = 's'
                        elif players[i].get_values() <= 7:
                            x = 'h'
                        else:
                            x = hard_totals[dealerUpcard][17-players[i].get_values()]
                    if x == 'ds' and len(players[i].cards) != 2:
                        x = 's'
                    elif x == 'ds':
                        x = 'd'
                    if x == 'd' and len(players[i].cards) != 2:
                        x = 'h'
                if self.displayMode:
                   print("auto choose", x)


                    
                #stand split hit double surrender
                if x == 'h':
                    players[i].add_card(self.deck.deal_card())
                elif x == 's':
                    break
                elif x == 'p':
                    assert len(players[i].cards) == 2, "player does not have 2 cards"
                    assert players[i].cards[0].value == players[i].cards[1].value
                    tempCard1 = players[i].cards[0]
                    tempCard2 = players[i].cards[1]
                    players.insert(i+1, Hand())
                    players[i+1].add_card(tempCard2)
                    players[i].clear_hand() 
                    players[i].add_card(tempCard1)

                    if players[i].cards[0].rank == 'A':
                        players[i].add_card(self.deck.deal_card())
                        players[i+1].add_card(self.deck.deal_card())
                        # End both hands after one card is dealt to each
                        i += 1
                        hands_total += 1
                        self.number_of_players += 1
                        break
                    else:
                        players[i].add_card(self.deck.deal_card())
                        hands_total += 1
                        self.number_of_players += 1
                elif x == 'd':
                    players[i].add_card(self.deck.deal_card())
                    players[i].bet *= 2
                    break
                else:
                    print("bad input. smth wrong")
                if players[i].get_values() > 21:
                    if self.displayMode:
                        print("player bust")
                    hand_over = True
                    self.display_all_hands(players,dealer)
                    break
                elif players[i].get_values() == 21:
                    if self.displayMode:
                        print("player 21")
                    break
                self.display_hands(players,dealer)

            i += 1
        while(hand_over == False):
            if dealer.get_values() <= 16:
                dealer.add_card(self.deck.deal_card())
            elif dealer.get_values() == 17 and dealer.softTotal:
                dealer.add_card(self.deck.deal_card())
            else:
                hand_over = True
                self.display_all_hands(players,dealer)
        for i in range(hands_total):
            if players[i].get_values() > 21:
                if self.displayMode:
                  print("player loses")
                self.bankroll -= players[i].bet*players[i].betMultiplier
                self.total_wagered += players[i].bet*players[i].betMultiplier
            elif dealer.get_values() > 21:
                if self.displayMode:
                    print("dealer bust")
                    print("player wins")
                self.bankroll += players[i].bet*players[i].betMultiplier
                self.total_wagered += players[i].bet*players[i].betMultiplier
            elif players[i].get_values() == dealer.get_values():
                if self.displayMode:
                 print("push")
            elif players[i].get_values() > dealer.get_values():
                if self.displayMode:
                   print("player wins")
                self.bankroll += players[i].bet*players[i].betMultiplier
                if players[i].betMultiplier == 1.5:
                    self.total_wagered += players[i].bet
                else:
                    self.total_wagered += players[i].bet*players[i].betMultiplier
            else:
                if self.displayMode:
                    print("player loses")
                self.bankroll -= players[i].bet*players[i].betMultiplier
                self.total_wagered += players[i].bet*players[i].betMultiplier
            if self.displayMode:
                print('\n')
        self.number_of_players = self.initial_number_of_players



times_gone_broke = 0
final_profit = []
hands_played = []
for i in range(1000): 
    sim = GameSimulator(2, True, 500, 0.25)
    sim.displayMode = False
    bankrollProgress = []

    shoesToPlay = 10

    betting_strategy = { # true count : bet
        0: 25,
        1: 25,
        2: 50,
        3: 50,
        4: 75,
        5: 75
    }

    goneBroke = False
    while sim.shoes_played <= shoesToPlay:

        # Calculate true count
        running_count = sim.deck.get_count()
        decks_remaining = sim.deck.get_cards_left() / 52
        if decks_remaining == 0:
            true_count = 0
        else:
            true_count = int(running_count / decks_remaining)
        def get_bet_from_true_count(true_count):
            if true_count <= 0:
                return betting_strategy[0]
            elif true_count >= 5:
                return betting_strategy[5]
            else:
                return betting_strategy.get(true_count)
        #print("count:", true_count, running_count)

        sim.play_hand(bet_input = get_bet_from_true_count(true_count))
        if sim.bankroll < 0:
            if not goneBroke:
                times_gone_broke += 1
                goneBroke = True
             #print("broke on hand:", sim.hands_played)
        #print("bankroll: $",sim.bankroll)
    hands_played.append(sim.hands_played)
    final_profit.append(sim.bankroll - sim.initial_bankroll)

    '''
    print(sim.hands_played, "hands played")
    house_edge = 100*(sim.initial_bankroll - sim.bankroll) / sim.total_wagered
    print("total win: ${0}".format(sim.bankroll - sim.initial_bankroll))
    print("house edge: {0}%".format(round(house_edge,8)))
    '''

sorted_final_profit = sorted(final_profit)
print("times gone broke:", times_gone_broke)
print("average profit: $", sum(final_profit)/len(final_profit))
print("worst result: $", min(final_profit))
print("10% bottom result: $", sorted_final_profit[len(final_profit)//10])
print("best result: $", max(final_profit))
print("10% top result: $", sorted_final_profit[len(final_profit)//10*9])
print("average hands played per session :", sum(hands_played)/len(hands_played))
