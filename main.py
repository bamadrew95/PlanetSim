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

    # Fonts
    self.default_font = pygame.font.Font('assets/fonts/Pixeltype.ttf', 24)

    # initial states
    self.click_pos = (0, 0)
    self.add_mode = False
    self.velocity_selector = (0, 0)

    # run game_files
    self.ui = UI()
    self.physics = Physics()

    # Sprite groups
    self.all_sprites = pygame.sprite.Group()
    self.collision_sprites = pygame.sprite.Group()
    self.satellites = pygame.sprite.Group()
    self.orbiting_sprites = pygame.sprite.Group()
    self.trail_sprites = pygame.sprite.Group()
    self.textboxes = pygame.sprite.Group()
    self.add_mode_arrow = pygame.sprite.GroupSingle()

    self.create_sprites = CreateSprites(self.all_sprites, self.collision_sprites, self.orbiting_sprites, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 750)

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
              self.ui.add_satellite([self.all_sprites, self.satellites], self.click_pos, self.velocity, self.rand_color, self.orbiting_sprites)
            else:
              self.add_mode = True
              self.click_pos = pygame.mouse.get_pos()
              self.rand_color = (randint(100, 255), randint(100, 255), randint(100, 255))

        # MENU EVENTS

      # End event loop

      # SIMULATOR GAME LOGIC
      if self.game_state == 'sim':
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        self.create_sprites.create_traildots([self.all_sprites, self.trail_sprites], self.satellites, self.trail_sprites)
        self.physics.collisions(self.satellites, self.orbiting_sprites)
        if self.add_mode:
          self.velocity = self.ui.add_mode(self.screen, self.click_pos, self.default_font, self.rand_color)

      pygame.display.update()
      
      self.clock.tick(self.framerate)

if __name__ == '__main__':
  game = Game()
  game.run()