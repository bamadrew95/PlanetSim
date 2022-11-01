import pygame, sys, time
from settings import *
from game_files.sprites import SimBG, Sun, Satellite, TrailDot
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
    self.enter_add_mode = False
    self.velocity_selector = (0, 0)

    # run game_files
    self.ui = UI()

    # Sprite groups
    self.all_sprites = pygame.sprite.Group()
    self.collision_sprites = pygame.sprite.Group()
    self.satellites = pygame.sprite.Group()
    self.non_orbiting_sprites = pygame.sprite.Group()
    self.trail_sprites = pygame.sprite.Group()
    self.add_mode_arrow = pygame.sprite.GroupSingle()

    # Initialize sprites
    bg = SimBG(self.all_sprites)
    sun = Sun([self.all_sprites, self.collision_sprites, self.non_orbiting_sprites], 25)
  
  def physics_simulator(self):
    self.satellites.update()

  def add_satellite(self, pos):
    Satellite([self.all_sprites, self.satellites], pos, self.velocity_selector, self.rand_color)

  def add_mode(self):
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.line(self.screen, self.rand_color, self.click_pos, mouse_pos, 4)

    self.velocity_meter(mouse_pos)
  
  def velocity_meter(self, mouse_pos):
    click_pos_vect = pygame.math.Vector2(self.click_pos)
    mouse_pos_vect = pygame.math.Vector2(mouse_pos)

    rel_vect = click_pos_vect - mouse_pos_vect

    distance = math.sqrt(math.pow(rel_vect.x, 2) + math.pow(rel_vect.y, 2))
    total_velocity = round(distance / 100, 2)

    self.velocity_selector = (-rel_vect.x / 100, -rel_vect.y / 100)

    surf = self.default_font.render(str(total_velocity), True, self.rand_color)

    if mouse_pos[0] >= self.click_pos[0]:
      rect = surf.get_rect(midright = (self.click_pos[0] - 10, self.click_pos[1]))
    else:
      rect = surf.get_rect(midleft = (self.click_pos[0] + 10, self.click_pos[1]))

    self.screen.blit(surf, rect)

  def draw_trails(self):
    for sprite in self.satellites:
      TrailDot([self.all_sprites, self.trail_sprites], sprite.color, sprite.pos)
    
    for sprite in self.trail_sprites:
      seconds = 10
      frames = seconds * FRAMERATE
      sprite.timer += 1
      if sprite.timer > frames:
        sprite.kill()

  def collisions(self):
    for sprite in self.satellites:
      if pygame.sprite.spritecollide(sprite, self.collision_sprites, False):
        sprite.kill()

  def run(self):
    while True:
      self.screen.fill((0,0,0))
      
      # event loop
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        
        if self.game_state == 'sim' and event.type == pygame.MOUSEBUTTONDOWN:
          if self.enter_add_mode:
            self.enter_add_mode = False
            self.add_satellite(self.click_pos)
          else:
            self.enter_add_mode = True
            self.click_pos = pygame.mouse.get_pos()
            self.rand_color = (randint(75, 255), randint(75, 255), randint(75, 255))
            

      # SIMULATOR GAME LOGIC
      if self.game_state == 'sim':
        self.physics_simulator()
        self.all_sprites.draw(self.screen)
        self.draw_trails()
        self.collisions()
        if self.enter_add_mode:
          self.add_mode()

      pygame.display.update()
      
      self.clock.tick(self.framerate)

if __name__ == '__main__':
  game = Game()
  game.run()