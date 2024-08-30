import pygame.font

from ship import Ship

class ScoreBoard:

    def __init__(self,ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.ship = pygame.image.load('images/ship_r_icon.png')
        self.ship_rect = self.ship.get_rect()
        self.screen_rect = ai_game.screen.get_rect()
        self.ship_rect.x = 10
        self.ship_rect.y = 10

        self.text_color = (200,200,200)
        self.font =pygame.font .SysFont(None, 50)

        self.prep_score()
        self.prep_highest_score()
        self.prep_level()
        self.prep_ship()

    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        formatted_score = "{:,}".format(rounded_score)
        score_str = str(f'Current Score: {formatted_score}')
        self.score_image = self.font.render(score_str,True,self.text_color,self.settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 30
        self.score_rect.top = 10

    def show_score(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.highest_score_image,self.highest_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.screen.blit(self.ship,self.ship_rect)
        self.screen.blit(self.ship_remain_image,self.ship_remain_rect)


    def prep_highest_score(self):
        highest_score = round(self.stats.highest_score, -1)
        formatted_highest_score = "{:,}".format(highest_score)
        highest_score_str = str(f'Highest Score: {formatted_highest_score}')
        self.highest_score_image = self.font.render(highest_score_str,True,self.text_color,self.settings.bg_color)

        self.highest_score_rect = self.highest_score_image.get_rect()
        self.highest_score_rect.centerx = self.screen_rect.centerx
        self.highest_score_rect.top = self.score_rect.top

    def check_highest_score(self):
        if self.stats.score > self.stats.highest_score:
            self.stats.highest_score = self.stats.score
            self.prep_highest_score()

    def prep_level(self):
        level_str = str(f'Level {self.stats.level}')
        self.level_image = self.font.render(level_str,True, self.text_color,self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left + 400
        self.level_rect.top = 10

    def prep_ship(self):
        ship_remain_str = str(f'x {self.stats.ship_left}')
        self.ship_remain_image = self.font.render(ship_remain_str,True,self.text_color,self.settings.bg_color)

        self.ship_remain_rect = self.ship_remain_image.get_rect()
        self.ship_remain_rect.left = self.screen_rect.left + 20 + self.ship_rect.width
        self.ship_remain_rect.top = 16

