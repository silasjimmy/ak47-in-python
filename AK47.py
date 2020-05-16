#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 08:34:49 2020

@author: silasjimmy
"""

import random
import os
from PIL import ImageTk, Image
import tkinter as tk
import tkinter.messagebox as msg

CARDS_FOLDER = os.path.join(os.getcwd(), "cards")

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
        Gets the pile's cards.
        Returns (list) the cards currently in the pile.
        '''
        return self.cards
    
    def get_top_card(self, remove=False):
        '''
        Returns (Card object) the top card in the pile.
        '''
        if remove:
            return self.cards.pop(-1)
        elif self.cards:
            return self.cards[-1]
        
    def add_card(self, card):
        '''
        Adds a card to the pile.
        card (Card): The card to add to the pile.
        '''
        self.cards.append(card)
        
    def draw_card(self):
        '''
        Removes a card from the top of the pile.
        Returns (Card) a card.
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
    
    def get_cards(self):
        '''
        Returns (Card) the cards in the hand.
        '''
        return self.cards
    
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
        Calculates and returns the value of the hand.
        '''
        self.value = 0
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                self.value += 10
        return self.value
    
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
        
    def need_discarded_card(self, discarded_card):
        if discarded_card in self.cards:
            return False
        elif discarded_card.value in ["A", "K", "4", "7"]:
            return True
        else:
            return False
        
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
        
    def play(self, drawn_card):
        '''
        Defines how the computer plays.
        Returns (Card object) the card played.
        '''
        # First add card to the hand
        self.cards.append(drawn_card)
        
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

class GameGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AK47")
        self.resizable(False, False)
        
        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 800) / 2
        y = (screen_height - 600) / 2
        self.geometry("%dx%d+%d+%d" % (800, 600, x, y))
        
        self.player_points = 0
        self.computer_points = 0
        self.player_points_string = tk.StringVar()
        self.computer_points_string = tk.StringVar()
        
        self.create_game_screen()
        
    def create_game_screen(self):
        '''
        Creates the game screen.
        '''
        # Create the game screen
        self.game_screen = tk.Frame(self, width=800, height=600, bg="green")
        self.game_screen.pack_propagate(0)
        
        # Create the points labels
        self.player_points_string.set("Player points: " + str(self.player_points))
        self.computer_points_string.set("Computer points: " + str(self.computer_points))
        self.player_points_label = tk.Label(self.game_screen, textvar=self.player_points_string, font="Arial 15 bold", fg="white", bg="green")
        self.comp_points_label = tk.Label(self.game_screen, textvar=self.computer_points_string, font="Arial 15 bold", fg="white", bg="green")
        
        # Create the draw pile, hands and discard pile
        self.draw_pile = DrawPile()
        self.draw_pile.shuffle()
        self.player = Hand(self.draw_pile.deal_player_cards())
        self.computer = Computer(self.draw_pile.deal_player_cards())
        self.discard_pile = DiscardPile()
        
        # Display the cards and points labels
        self.display_computer_cards()
        self.display_draw_pile()
        self.display_discard_pile(f_time=True)
        self.display_player_cards(f_time=True)
        self.player_points_label.pack(side=tk.RIGHT, anchor=tk.S, padx=(0, 20), pady=(0, 15))
        self.comp_points_label.pack(side=tk.LEFT, anchor=tk.N, padx=(20, 0), pady=(15, 0))
        
        self.card_drawn = False
        self.game_screen.pack(side=tk.LEFT, anchor=tk.N)
        
    def display_computer_cards(self, reveal_cards=False):
        '''
        Displays the computer cards.
        '''
        computer_cards = self.computer.get_cards()
        if reveal_cards:
            card_image_names = [self.card_png_name(card) for card in computer_cards]
            self.computer_card_images = [ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/" + card_name)) for card_name in card_image_names]
        else:
            self.computer_card_images = [ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/back.png")) for i in range(len(computer_cards))]
        self.computer_card_image_labels = [tk.Label(self.game_screen, image=card_image) for card_image in self.computer_card_images]
        
        # Centering the cards horizontally
        card_width = self.computer_card_image_labels[0].winfo_reqwidth()
        card_spacing = 30
        cards_length = ((len(computer_cards) - 1) * card_spacing) + card_width
        remaining_window_space = self.game_screen.winfo_reqwidth() - cards_length
        x_start = remaining_window_space / 2
        
        for index, card_image_label in enumerate(self.computer_card_image_labels):
            pad = index * card_spacing
            card_image_label.place(x=x_start+pad, y=50)
    
    def display_draw_pile(self):
        '''
        Displays the draw pile.
        '''
        self.draw_pile_png = ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/back.png"))
        self.draw_pile_label = tk.Label(self.game_screen, image=self.draw_pile_png)
        self.draw_pile_label.bind("<Button-1>", self.draw_card)
        
        card_height = self.draw_pile_label.winfo_reqheight()
        occupied_space = (card_height * 2) + 100
        remaining_window_space = self.game_screen.winfo_reqheight() - occupied_space
        y = card_height + (remaining_window_space / 2)
        
        self.draw_pile_label.place(x=100, y=y)
    
    def display_discard_pile(self, f_time=False):
        '''
        Displays the discard pile.
        '''
        if f_time:
            self.discard_pile_label = tk.Canvas(self.game_screen, width=82, height=113, bg="grey")
        else:
            self.discard_pile_label.destroy()
            top_card_png_name = self.card_png_name(self.discard_pile.get_top_card())
            self.discard_pile_png = ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/" + top_card_png_name))
            self.discard_pile_label = tk.Label(self.game_screen, image=self.discard_pile_png)
            
        card_height = self.draw_pile_label.winfo_reqheight()
        card_width = self.discard_pile_label.winfo_reqwidth()
        occupied_space = (card_height * 2) + 100
        remaining_window_space = self.game_screen.winfo_reqheight() - occupied_space        
        x = self.game_screen.winfo_reqwidth() - (card_width + 100)
        y = card_height + (remaining_window_space // 2)
        
        self.discard_pile_label.bind("<Button-1>", self.pick_discarded_card)
        self.discard_pile_label.place(x=x, y=y)
    
    def display_player_cards(self, f_time=False):
        '''
        Displays the player cards.
        '''
        # Destroy the images if they already exist
        if not f_time:
            for label in self.player_card_image_labels:
                label.destroy()
                
        player_cards = self.player.get_cards()
        card_image_names = [self.card_png_name(card) for card in player_cards]
        self.player_card_images = [ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/" + card_name)) for card_name in card_image_names]
        self.player_card_image_labels = [tk.Label(self.game_screen, image=card_image) for card_image in self.player_card_images]
        
        # Centering the cards horizontally
        card_width = self.player_card_image_labels[0].winfo_reqwidth()
        card_height = self.player_card_image_labels[0].winfo_reqheight()
        card_spacing = 30
        cards_length = ((len(player_cards) - 1) * card_spacing) + card_width
        remaining_window_space = self.game_screen.winfo_reqwidth() - cards_length
        x_start = remaining_window_space / 2
        y_start = self.game_screen.winfo_reqheight() - (card_height + 50)
        
        for index, card_image_label in enumerate(self.player_card_image_labels):
            self.make_dragable(card_image_label)
            pad = index * card_spacing
            card_image_label.place(x=x_start+pad, y=y_start)
    
    def card_png_name(self, card):
        '''
        Creates the card's png image name.
        card (Card): A card.
        Returns (str) the name of the card's image name.
        '''
        return card.suit + card.value + ".png"
    
    def draw_card(self, event):
        '''
        Adds a card from the draw pile to the hand.
        '''
        if self.draw_pile.is_empty():
            # Get the remaining cards from the discard and draw piles and add them together
            all_cards = self.discard_pile.get_cards() + self.draw_pile.get_cards()
            # Create a new draw pile with the remaining cards from discard and draw pile
            self.draw_pile = DrawPile(other_cards=all_cards)
            self.draw_pile.shuffle()
            # Create a new discard pile and display it
            self.discard_pile = DiscardPile()
            self.display_discard_pile(f_time=True)
            
        if not self.card_drawn:
            drawn_card = self.draw_pile.draw_card()
            self.player.add_card(drawn_card)
            self.display_player_cards()
            self.card_drawn = True
        else:
            msg.showerror("AK47", "You can't draw more than one card. Drop a card first to draw another.")
        
    def pick_discarded_card(self, event):
        '''
        Adds a card from the discard pile to the hand.
        '''
        if not self.card_drawn:
            drawn_card = self.discard_pile.get_top_card(remove=True)
            self.player.add_card(drawn_card)
            self.display_discard_pile()
            self.display_player_cards()
            self.card_drawn = True
        else:
            msg.showerror("AK47", "You can't draw more than one card. Drop a card first to draw another.")
            
    def hand_over(self, hand_winner):
        '''
        Shows message when a hand is over.
        hand_winner (str): The winner of the hand.
        '''
        # Reveal computer's cards
        self.display_computer_cards(reveal_cards=True)
        
        if hand_winner == "player":
            message = "Congratulations!! You win the hand"
            points = self.computer.get_hand_value()
            self.player_points += points
        else:
            message = "Aaw, sorry mate you lost to the computer"
            points = self.player.get_hand_value()
            self.computer_points += points
            
        if self.player_points >= 100 or self.computer_points >= 100:
            if self.player_points >= 100:
                self.game_over("player")
            else:
                self.game_over("computer")
        else:
            new_hand = msg.askquestion("Hand over!", message + " with " + str(points) + " points. Play another hand?")
            
            if new_hand == "yes":
                self.player_points_string.set("Player points: " + str(self.player_points))
                self.computer_points_string.set("Computer points: " + str(self.computer_points))
                self.game_screen.destroy()
                self.create_game_screen()
            else:
                msg.showinfo("AK47", "Bye bye and thanks for playing the game!")
                self.after(400, self.destroy)
            
    def game_over(self, game_winner):
        '''
        Ends the game and starts a new one or quits the game.
        game_winner (str): Winner of the game.
        '''
        if game_winner == "player":
            message = "Congratulations!!! You win the game with " + str(self.player_points)
        else:
            message = "Oopsy! Sorry but the computer beat you in this with " + str(self.computer_points)
            
        new_game = msg.askquestion("Game over!", message + ". Play a new game?")
        if new_game == "yes":
            self.player_points, self.computer_points = 0, 0
            self.player_points_string.set("Player points: " + str(self.player_points))
            self.computer_points_string.set("Computer points: " + str(self.computer_points))
            self.game_screen.destroy()
            self.create_game_screen()
        else:
            msg.showinfo("AK47", "Bye bye and thanks for playing the game!")
            self.after(400, self.destroy)
    
    def on_drag_start(self, event):
        '''
        Triggered when the card is clicked.
        '''
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y
        
        # Card's original coords
        self.original_x = widget.winfo_x()
        self.original_y = widget.winfo_y()
        
    def on_drag_motion(self, event):
        '''
        Triggered when the card is dragged across the window.
        '''
        widget = event.widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        
        if self.card_drawn:
            # Define the window boundary of the drag and drop
            x_boundary = 800 - widget.winfo_width()
            y_boundary = 600 - widget.winfo_height()
            if (x > 0 and x < x_boundary) and (y > 0 and y < y_boundary):
                widget.place(x=x, y=y)
        else:
            msg.showerror("AK47", "Draw a card first before you can make a drop.")
            
    def on_drag_release(self, event):
        '''
        Triggered when the card is released.
        '''
        widget = event.widget
        x = widget.winfo_x()
        y = widget.winfo_y()
        
        if (x > 546 and x < 690) and (y > 147 and y < 353):
            card_position = self.player_card_image_labels.index(widget)
            dropped_card = self.player.drop_card(card_position)
            self.discard_pile.add_card(dropped_card)
            self.display_discard_pile()
            self.display_player_cards()
            self.card_drawn = False
            
            if self.player.hand_over():
                self.hand_over("player")
            
            ## Computer's turn ##
            top_card = self.discard_pile.get_top_card()
            if top_card:
                if self.computer.need_discarded_card(top_card):
                    drawn_card = self.discard_pile.get_top_card(remove=True)
                    self.display_discard_pile()
                else:
                    drawn_card = self.draw_pile.draw_card()
            else:
                drawn_card = self.draw_pile.draw_card()
                
            dropped = self.computer.play(drawn_card)
            self.discard_pile.add_card(dropped)
            self.display_discard_pile()
            self.display_computer_cards()
            self.display_player_cards()
            
            if self.computer.hand_over():
                self.hand_over("computer")
        else:
            widget.place(x=self.original_x, y=self.original_y)
            
    def make_dragable(self, widget):
        '''
        Makes the card draggable.
        '''
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)
        widget.bind("<ButtonRelease-1>", self.on_drag_release)