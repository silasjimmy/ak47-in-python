#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 07:43:44 2020

@author: silasjimmy
"""

from AK47 import DiscardPile, DrawPile, Hand, Computer
    
class Game:
    def __init__(self):
        print("######################")
        print("######## AK47 ########")
        print("######################")
        print("\nWelcome to the card game AK47!")
        print("\n*** The goal is to get cards with values A, K, 4 and 7. The first player to get the cards wins the hand. ***")
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
        computer_cards = draw_pile.deal_player_cards()
        
        # Create players' hands
        player = Hand(player_cards)
        computer = Computer(computer_cards)
        
        # Game variables
        self.winner = None
        self.winner_points = 0
        
        while not player.hand_over() and not computer.hand_over():
            # First check if the draw pile is empty
            if draw_pile.is_empty():
                # Get the remaining cards from the discard and draw piles and add them together
                discard_pile_cards = discard_pile.get_cards()
                draw_pile_cards = draw_pile.get_cards()
                all_cards = discard_pile_cards + draw_pile_cards
                
                # Create a new draw pile with the remaining cards from discard and draw pile
                draw_pile = DrawPile(other_cards=all_cards)
                draw_pile.shuffle()
                
                # Create a new discard pile
                discard_pile = DiscardPile()
                
            # Display computer cards
            print("\n*** Computer's cards are hidden. ***")
            # Display the player's hand
            print("\n#### Your cards ####")
            player.display_hand()
            
            #### Player's turn ####
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
            
            if player.hand_over():
                self.winner = "player"
                break
            
            #### Computer's turn ####
            dropped = computer.play()
            # Add the card to the discard pile
            discard_pile.add_card(dropped)
            # Draw a card from the draw pile and add to the hand
            draw = draw_pile.draw_card()
            computer.add_card(draw)
            print("\n*** Computer  dropped", dropped, "and drew a card ***")
            
            if player.hand_over():
                self.winner = "computer"
                break
            
        print("\n######################")
        print("#### Hand over! ######")
        print("######################")
              
        # Print opponent's hand
        print("\nOpponent's cards:")
        if self.winner == "player":
            computer.display_hand()
            self.winner_points = computer.get_hand_value()
        else:
            player.display_hand()
            self.winner_points = player.get_hand_value()
            
        print("\n The", self.winner, "wins the hand with", self.winner_points, "points!")
        
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

if __name__ == "__main__":        
    game = Game()

#comp = Computer([Card("Spades", "A"), Card("Diamonds", "K"), Card("Clubs", "4"), Card("Hearts", "7")])
#comp.display_hand()
#c = comp.get_hand_value()
#print(c)






