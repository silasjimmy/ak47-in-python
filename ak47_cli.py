#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 07:43:44 2020

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
        for card in self.cards:
            if card.value.isnumeric():
                if int(card.value) == 8:
                    self.value += 50
                else:
                    self.value += int(card.value)
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
    
class Game:
    def __init__(self):
        print("######################")
        print("######## AK47 ########")
        print("######################")
        print("\nWelcome to the card game AK47!")
        print("\nStart the game!")
        print("\n######################")
        
        self.play_game()
        
    def play_game(self):
        # Create and shuffle the draw pile
        draw_pile = DrawPile()
        draw_pile.shuffle()
        
        # Create the discard pile
        discard_pile = DiscardPile()
        
        # Deal each player 7 cards and create their hands
        player_cards = draw_pile.deal_player_cards()
        player = Hand(player_cards)
        
        while not player.hand_over():
            # Display the player's hand
            print("\n#### Your cards ####")
            player.display_hand()
            
            # Drop a card of your choice
            num = self.prompt_card_num(player)
            # Get the card dropped
            dropped = player.drop_card(num)
            
            # Add the card to the discard pile
            discard_pile.add_card(dropped)
            print("\n>>> You  dropped", dropped)
    
            # Draw a card from the draw pile and add to the hand
            draw = draw_pile.draw_card()
            player.add_card(draw)
            print("\n>>> You drew", draw)
            # Do that until you get AK47
        
    def prompt_card_num(self, hand):
        '''
        Prompts the player to enter a card number to drop.
        Returns (int) the number entered.
        '''
        valid_card_numbers = [str(i) for i in range(hand.get_num_of_cards())]
        num = input("Enter the number of the card to drop: ")
        while not num.isdigit() or num not in valid_card_numbers:
            num = input("Please enter a valid card number: ")
        return int(num)
        
game = Game()