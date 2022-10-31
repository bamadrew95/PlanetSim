import pygame, sys, time
from settings import *
from game_files.sprites import BG, Sun, Satellite, TrailDot
import math
from random import randint

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

    # Sprite groups
    self.all_sprites = pygame.sprite.Group()
    self.collision_sprites = pygame.sprite.Group()
    self.satellites = pygame.sprite.Group()
    self.non_orbiting_sprites = pygame.sprite.Group()
    self.trail_sprites = pygame.sprite.Group()

    self.trail_sprite = pygame.sprite.Group()

    # Initialize sprites
    bg = BG(self.all_sprites)
    sun = Sun([self.all_sprites, self.collision_sprites, self.non_orbiting_sprites], 25)
  
  def physics_simulator(self):
    self.all_sprites.update()

  def add_satellite(self, pos):
    Satellite([self.all_sprites, self.satellites], pos, (1.75, 0), (randint(0, 255), randint(0, 255), randint(0, 255)))
  
  def draw_trails(self):
    for sprite in self.satellites:
      TrailDot([self.all_sprites, self.trail_sprites], sprite.color, sprite.pos)
    
    for sprite in self.trail_sprites:
      sprite.time += 1
      if sprite.time > 200:
        sprite.kill()

  def collisions(self):
    for sprite in self.satellites:
      if pygame.sprite.spritecollide(sprite, self.collision_sprites, False):
        sprite.kill()

  def run(self):
    while True:
      # self.screen.fill((0,0,0))
      
      # event loop
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        
        if self.game_state == 'sim' and event.type == pygame.MOUSEBUTTONDOWN:
          self.add_satellite(pygame.mouse.get_pos())

      # check game state
      if self.game_state == 'sim':
        self.physics_simulator()
        self.all_sprites.draw(self.screen)
        self.draw_trails()
        self.collisions()

      pygame.display.update()
      self.clock.tick(self.framerate)

if __name__ == '__main__':
  game = Game()
  game.run()