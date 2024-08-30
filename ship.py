import pygame


class Ship:

    def __init__(self,ai_game):
        """initialize the ship and setting its position"""

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # load ship image and acquire its rectangle perimeter
        self.image = pygame.image.load('images/ship_r.png')
        self.rect = self.image.get_rect()

        # for every new ship, put it at the middle of the screen bottom
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left = False
        self.moving_forward = False
        self.moving_backward = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        if self.moving_forward and self.rect.top > self.settings.ship_upper_boundary:
            self.y -= self.settings.ship_speed
        if self.moving_backward and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y


    def blitme(self):
        """put the ship at the right location"""
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y - float(self.rect.y)