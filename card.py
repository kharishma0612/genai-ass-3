import random
import pygame
import english_text as lang

class Suits:
  """Represents a suit of cards"""
  def __init__(self, name):
    self.name = name
    self.cards = []
    self.add_cards()

    
  def add_cards(self):
    values = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    for value in values:
        self.cards.append(Card(self.name, value))
  def __str__(self):
    return lang.suit_name

class DiamondSuit(Suits):
  """Represents the diamond suit with shuffling capability"""
  def __init__(self):
    super().__init__(lang.DIAMONDS)  # Call parent class constructor
    self.shuffle()

  def shuffle(self):
    """Shuffles the cards in the diamond suit"""
    random.shuffle(self.cards)


class Card:
  """Represents a single playing card"""
  suits = (lang.SPADES, lang.HEARTS, lang.DIAMONDS, lang.CLUBS)
  values = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
  def __init__(self, suit, value):
    if suit not in Card.suits or value not in Card.values:
      raise ValueError(lang.INVALID_CARD_ERROR)
    self.suit = suit
    self.value = value
    self.image_path = ('img/'+str(self.value) + str(self.suit[0]) + '.png')
    self.rect = None
    self.img = None

  def __eq__(self, other):
    return self.suit == other.suit and self.value == other.value

  def __str__(self):
    """Returns a string representation of the card"""
    higher_card_names = lang.HIGHER_CARD_NAMES
    face_value = higher_card_names[self.value - 11] if self.value > 10 else self.value
    return lang.card_name(face_value, self.suit)
  
  def display_card(self, screen, x, y, width, height):
    image_original = pygame.image.load(self.image_path).convert_alpha()
    self.img = pygame.transform.scale(image_original, (width, height))
    self.rect = self.img.get_rect()
    self.rect.width = width
    self.rect.height = height
    self.img.fill((255, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)

    self.x, self.y = x, y
    self.width, self.height = width, height
    
    screen.blit(self.img, (x, y))

  def is_clicked(self, pos):
    """Check if the card is clicked"""
    x_loc, y_loc = pos

    in_x = 0 <= (x_loc - self.x) <= self.width
    in_y = 0 <= (y_loc - self.y) <= self.height
    
    return in_x and in_y

c1 = Card("Spades", 12)
c2 = Card("Spades", 12)
print(c1 == c2)
