#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 08:34:49 2020

@author: silasjimmy
"""

import random

class Card:
    '''
    Defines a card.
    '''
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
    def __str__(self):
        return " of ".join((self.value, self.suit))
    
class DiscardPile:
    '''
    Defines a discard pile.
    '''
    def __init__(self, other_cards=None):
        if other_cards:
            self.cards = other_cards
        else:
            self.cards = []
        
    def get_cards(self):
        '''
        Gets the pile's cards
        Returns (list of Card objects) the pile's cards.
        '''
        return self.cards
    
    def get_top_card(self):
        '''
        Returns (Card object) the top card in the pile.
        '''
        return self.cards[-1]
        
    def add_card(self, card):
        '''
        Adds a card to the pile.
        card (Card object): The card to add to the pile.
        '''
        self.cards.append(card)
        
    def draw_card(self):
        '''
        Removes a card from the top of the pile.
        Returns (Card object) a card.
        '''
        if len(self.cards) > 1:
            return self.cards.pop(-1)
        
    def shuffle(self):
        '''
        Shuffles the pile.
        '''
        if len(self.cards) > 1:
            random.shuffle(self.cards)
            
    def is_empty(self):
        '''
        Checks if the pile has less than 2 cards to declare empty.
        Returns True if it is, False otherwise.
        '''
        if len(self.cards) < 2:
            return True
        return False
            
class DrawPile(DiscardPile):
    '''
    Defines a draw pile
    '''
    def __init__(self, other_cards=None):
        super().__init__()
        if other_cards:
            self.cards = other_cards
        else:
            self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts", "Diamonds"] 
                                    for v in ["A", "2", "3", "4", "5", "6", "7", "8", 
                                    "9", "10", "J", "Q", "K"]]
            
    def deal_player_cards(self):
        '''
        Deals the players with 4 cards.
        Returns (list of Cards) cards dealt.
        '''
        return [self.cards.pop(i) for i in range(4)]
        
class Hand:
    '''
    Defines a hand
    '''
    def __init__(self, cards):
        self.cards = cards
        self.value = 0
        
    def get_num_of_cards(self):
        '''
        Returns (int) the number of cards in the hand.
        '''
        return len(self.cards)
    
    def get_card(self, position):
        '''
        Returns (Card object) the card at the specified position.
        '''
        return self.cards[position]
    
    def add_card(self, card):
        '''
        Adds a card to the hand.
        card (Card object): The card to add.
        '''
        self.cards.append(card)
        
    def drop_card(self, num):
        '''
        Removes a card at the position specified with num.
        num (int): The position of the card to remove.
        Returns (Card object) the card removed.
        '''
        dropped_card = self.cards.pop(num)
        return dropped_card
    
    def get_hand_value(self):
        '''
        Returns (int) the value of the hand.
        '''
        self.calculate_hand_value()
        return self.value
        
    def calculate_hand_value(self):
        '''
        Calculates the value of the hand.
        '''
        self.value = 0
        card_values = set([card.value for card in self.cards])
        for value in card_values:
            if value in ["A", "K", "4", "7"]:
                if value.isnumeric():
                    self.value += int(value)
                else:
                    self.value += 10
    
    def display_hand(self):
        '''
        Displays the hand.
        '''
        for i, card in enumerate(self.cards):
            print("({}) -> {}".format(i, card))
            
    def hand_over(self):
        '''
        Checks if the hand is over or not.
        Returns True if it is, False otherwise.
        '''
        card_values = [card.value for card in self.cards]
        card_values = set(card_values)
        has_ak47 = False
        if len(card_values) == 4:
            for card_value in card_values:
                if card_value in ["A", "K", "4", "7"]:
                    has_ak47 = True
                else:
                    has_ak47 = False
                    break
            if has_ak47:
                return True
        return False
    
class Computer(Hand):
    '''
    Defines the computer's hand.
    '''
    def __init__(self, cards):
        super().__init__(cards)
        
    def num_of_value_occurrences(self):
        '''
        Gets the number of occurrences of cards with the same value.
        Returns (dict) each value with the number of occurrences.
        '''
        cards_occurrence = {}
        for card in self.cards:
            cards_occurrence[card.value] = len([c for c in self.cards if c.value == card.value])
        return cards_occurrence
    
    def card_with_value(self, value):
        '''
        Gets the card with the specified value.
        Returns (Card object) a card with the value specified.
        '''
        for index, card in enumerate(self.cards):
            if card.value == value:
                card_with_value = self.drop_card(index)
                return card_with_value
        
    def play(self):
        '''
        Defines how the computer plays.
        Returns (Card object) the card played.
        '''
        # Play if has a playable card
        for index, card in enumerate(self.cards):
            if card.value not in ["A", "K", "4", "7"]:
                dropped = self.drop_card(index)
                return dropped
        # Play if has no playable card but a repeated card
        value_occurrences = self.num_of_value_occurrences()
        for value in value_occurrences:
            if value_occurrences[value] > 1:
                return self.card_with_value(value)