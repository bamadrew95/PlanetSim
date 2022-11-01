import pygame, sys, time
from settings import *
from game_files.sprites import CreateSprites
from game_files.physics import Physics
from game_files.ui import UI
from random import randint
import math

class Game():
  def __init__(self):
    # import settings
    self.window_width = WINDOW_WIDTH
    self.window_height = WINDOW_HEIGHT
    self.framerate = FRAMERATE
    self.game_state = INITIAL_GAME_STATE

    # Initialization of pygame window
    pygame.init()
    self.screen = pygame.display.set_mode((self.window_width, self.window_height))
    pygame.display.set_caption('Planet Simulator')
    self.clock = pygame.time.Clock()


    # Cursors
    self.default_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
    self.pointer_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
    pygame.mouse.set_cursor(self.default_cursor)

    # Fonts
    self.default_font = pygame.font.Font('assets/fonts/Pixeltype.ttf', 24)

    # initial states
    self.paused = False
    self.click_pos = (0, 0)
    self.add_mode = False
    self.velocity_selector = (0, 0)

    # run game_files
    self.ui = UI()
    self.physics = Physics()

    # Sprite groups
    self.all_sprites = pygame.sprite.Group()
    self.menu_sprites = pygame.sprite.Group()
    self.menu_button_sprites = pygame.sprite.Group()
    self.sim_sprites = pygame.sprite.Group()
    self.collision_sprites = pygame.sprite.Group()
    self.satellite_sprites = pygame.sprite.Group()
    self.orbiting_sprites = pygame.sprite.Group()
    self.trail_sprites = pygame.sprite.Group()
    self.add_mode_arrow = pygame.sprite.GroupSingle()

    self.create_sprites = CreateSprites([self.all_sprites, self.sim_sprites], [self.all_sprites, self.sim_sprites, self.orbiting_sprites], (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 750)
    self.create_sprites.create_main_menu([self.all_sprites, self.menu_sprites], [self.all_sprites, self.menu_sprites, self.menu_button_sprites])

  def run(self):
    while True:
      self.screen.fill((0,0,0))
      
      # event loop
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

        # SIMULATOR EVENTS
        if self.game_state == 'sim':
          if event.type == pygame.MOUSEBUTTONDOWN:
            if self.add_mode:
              self.add_mode = False
              self.ui.add_satellite([self.all_sprites, self.sim_sprites, self.satellite_sprites], self.click_pos, self.velocity, self.rand_color, self.orbiting_sprites)
            else:
              self.add_mode = True
              self.click_pos = pygame.mouse.get_pos()
              self.rand_color = (randint(100, 255), randint(100, 255), randint(100, 255))
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
              if self.paused:
                self.paused = False
              else:
                self.paused = True

        # MENU EVENTS
        if self.game_state == 'menu':
          for button in self.menu_button_sprites:
            if button.hover and event.type == pygame.MOUSEBUTTONDOWN:
              if button.id == 1001:
                self.game_state = 'sim'

      # End event loop

      # SIMULATOR GAME LOGIC
      if self.game_state == 'sim':
        if not self.paused:
          self.physics.collisions(self.satellite_sprites, self.orbiting_sprites)
          self.create_sprites.create_traildots([self.all_sprites, self.sim_sprites, self.trail_sprites], self.satellite_sprites, self.trail_sprites)
          self.sim_sprites.update()
        self.sim_sprites.draw(self.screen)
        
        if self.add_mode:
          self.velocity = self.ui.add_mode(self.screen, self.click_pos, self.default_font, self.rand_color)

      # MENU LOGIC
      if self.game_state == 'menu':
        self.ui.detect_hover(self.menu_button_sprites, self.default_cursor, self.pointer_cursor)
        self.menu_sprites.update()
        self.menu_sprites.draw(self.screen)

      pygame.display.update()
      self.clock.tick(self.framerate)

if __name__ == '__main__':
  game = Game()
  game.run()