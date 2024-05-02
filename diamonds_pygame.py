import pygame
from diamonds_game import *
from pygame_display import *

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 600
CARD_WIDTH, CARD_HEIGHT = 80, 120
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50

MARGIN = 20

BACKGROUND_COLOR = GREEN

class Diamonds_PyGame:
    
    def __init__(self, screen):   
        self.NUM_ROUNDS = 13
        self.game = DiamondsGame()
        self.screen = screen
        clear_to_main_background(self.screen)
    
    def add_players(self, num_bots: int, num_randoms: int, human_names: list[str]):
        for human_name in human_names:
            self.game.add_human_player(human_name)

        for random in range(num_bots):
            self.game.add_bot()
        
        for random in range(num_randoms):
            self.game.add_random()
        

        
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
running = True

human_names, num_bots, num_randoms = player_configuration(screen)

py_game = Diamonds_PyGame(screen)

py_game.add_players(num_bots, num_randoms, human_names)
py_game.game.setup_game()

opponent = py_game.game.players[0]
on_round = 1

player_choose_card = 0
bids = []
highest_bid = 0
winners = []

gameplay = True
gui_choose = False
round_score_screen = False
final_score_screeen = False

revealed_diamond = py_game.game.diamond_pile.pop(0)
py_game.game.revealed_diamonds.append(revealed_diamond.value)

while running:

    if on_round > py_game.NUM_ROUNDS:
        display_final_scores(py_game.game.players, screen)

    if player_choose_card == len(py_game.game.players):
        gameplay = False
        round_score_screen = True
        points_given = revealed_diamond.value / len(winners)
        for winner in winners:
            winner.score += points_given
        
        player_choose_card = 0
        display_bids_and_winners(screen, bids, py_game.game.players, winners, highest_bid, on_round, revealed_diamond.value)

    
    if gameplay:
        clear_to_main_background(screen)
        
        print_round_title(screen, on_round, SCREEN_WIDTH)
        display_scores_on_main(screen, py_game.game.players)
        
        if opponent:
            opponent_hand = opponent.get_hand_values()

        player = py_game.game.players[player_choose_card]
        if player.isBot and opponent_hand:
            bid = player.choose_bid(revealed_diamond, py_game.game.revealed_diamonds, opponent_hand)
            player_choose_card += 1
            bids.append(bid)
            if bid.value > highest_bid:
                winners = [player]
                highest_bid = bid.value
            elif bid.value == highest_bid:
                winners.append(player)

        elif player.isRandom:
            bid = player.choose_bid()
            player_choose_card += 1

            bids.append(bid)
            if bid.value > highest_bid:
                winners = [player]
                highest_bid = bid.value
            elif bid.value == highest_bid:
                winners.append(player)
        else:
            revealed_diamond.display_card(screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, CARD_WIDTH, CARD_HEIGHT, )
            display_player_hand(player.hand, CARD_WIDTH, CARD_HEIGHT, screen, player.name)

            gui_choose = True
            gameplay = False
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gui_choose:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    player = py_game.game.players[player_choose_card]
                    for card in player.hand:
                        if card.is_clicked(mouse_pos):
                            player.hand.remove(card)
                            bid = card
                            
                            bids.append(bid)
                            
                            if bid.value > highest_bid:
                                winners = [player]
                                highest_bid = bid.value
                            elif bid.value == highest_bid:
                                winners.append(player)
                            
                            player_choose_card += 1
                            gui_choose = False
                            gameplay = True
                            break

            if round_score_screen:
                on_round += 1
                bids = []
                highest_bid = 0
                winners = []
                gameplay = True
                
                if on_round <= py_game.NUM_ROUNDS:
                    revealed_diamond = py_game.game.diamond_pile.pop(0)
                    py_game.game.revealed_diamonds.append(revealed_diamond.value)

                round_score_screen = False

pygame.quit()