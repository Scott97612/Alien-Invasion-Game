import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from background import Moon,Jupiter,Saturn
from button import Button
from score_board import ScoreBoard

class AlienInvasion:
    """managing game resources and behavior"""
    def __init__(self):
        """initialize game and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.stats = GameStats(self)
        self.play_button = Button(self,'Play(Press ENTER)')

        pygame.display.set_caption('Alien Invasion')
        self.bg = pygame.image.load('images/space.jpeg')
        self.sb = ScoreBoard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.moon = Moon(self)
        self.jupiter = Jupiter(self)
        self.saturn = Saturn(self)

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.fire = pygame.mixer.Sound('sound/fire.wav')
        self.explosion = pygame.mixer.Sound('sound/explosion.wav')
        self.victory = pygame.mixer.Sound('sound/victory.wav')
        self.fail = pygame.mixer.Sound('sound/fail.wav')

    def run_game(self):
        """begin the main loop of the game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()



    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._save_highest()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
               self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _save_highest(self):
        filename = 'save_highest_score.txt'

        with open(filename,'w') as file_object:
            file_object.write(str(self.stats.highest_score))

    def _check_keydown_events(self,event):
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_w:
            self.ship.moving_forward = True
        elif event.key == pygame.K_s:
            self.ship.moving_backward = True
        elif event.key == pygame.K_ESCAPE:
            self._save_highest()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            self._fire_bullet_sound()

        if not self.stats.game_active and event.key == pygame.K_KP_ENTER:
            self.stats.game_active = True
        elif not self.stats.game_active and event.key == pygame.K_RETURN:
            self.stats.game_active = True

    def _check_keyup_event(self,event):
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_forward = False
        elif event.key == pygame.K_s:
            self.ship.moving_backward = False

    def _fire_bullet_sound(self):
        pygame.mixer.Sound.play(self.fire)

    def _explosion_sound(self):
        pygame.mixer.Sound.play(self.explosion)

    def _win_sound(self):
        pygame.mixer.Sound.play(self.victory)

    def _lose_sound(self):
        pygame.mixer.Sound.play(self.fail)

    def _check_play_button(self,mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self._explosion_sound()
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_highest_score()
        if not self.aliens:
            self.bullets.empty()
            sleep(1.0)
            self._win_sound()
            sleep(1.0)
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (4 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (4 * alien_height) - ship_height)
        number_rows = available_space_y // (3 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._explosion_sound()
            self._lose_round()

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _lose_round(self):
        if self.stats.ship_left > 0:
            self._lose_sound()
            self.stats.ship_left -= 1
            self.sb.prep_ship()
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(3.0)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._lose_round()
                break

    def _update_screen(self):
        self.screen.blit(self.bg,(0,0))
        self.moon.blitmoon()
        self.jupiter.blitjupiter()
        self.saturn.blitsaturn()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


