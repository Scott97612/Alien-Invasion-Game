import pygame
from random import randint

class Moon:

    def __init__(self,ai_game):
        self.screen = ai_game.screen
        self.moon = pygame.image.load('images/moon.png')
        self.moon_rect = self.moon.get_rect()
        self.screen_rect = ai_game.screen.get_rect()

        self.moon_rect.x = randint(100,self.screen.get_rect().width - 100)
        self.moon_rect.y = randint(100, self.screen.get_rect().height - 100)

    def blitmoon(self):
        self.screen.blit(self.moon, self.moon_rect)

class Jupiter:

    def __init__(self,ai_game):
        self.screen = ai_game.screen
        self.jupiter = pygame.image.load('images/jupiter.png')
        self.jupiter_rect = self.jupiter.get_rect()
        self.screen_rect = ai_game.screen.get_rect()

        self.jupiter_rect.x = randint(200,self.screen.get_rect().width - 200)
        self.jupiter_rect.y = randint(200, self.screen.get_rect().height- 200)

    def blitjupiter(self):
        self.screen.blit(self.jupiter, self.jupiter_rect)

class Saturn:

    def __init__(self,ai_game):
        self.screen = ai_game.screen
        self.saturn = pygame.image.load('images/saturn.png')
        self.saturn_rect = self.saturn.get_rect()
        self.screen_rect = ai_game.screen.get_rect()

        self.saturn_rect.x = randint(150,self.screen.get_rect().width - 150)
        self.saturn_rect.y = randint(150, self.screen.get_rect().height - 150)

    def blitsaturn(self):
        self.screen.blit(self.saturn, self.saturn_rect)