import pygame
from settings import *
from game_files.physics import Physics
import math
from random import randint

class CreateSprites:
  def __init__(self, bg_groups: list, sun_groups: list, sun_pos: tuple, sun_mass: int):
    self.create_bg(bg_groups)
    self.create_sun(sun_groups, sun_pos, sun_mass)       
    
  def create_main_menu(self, bg_groups: list, button_groups: list):
    MenuBG(bg_groups)
    MenuButton(button_groups, 1001, 'Start Simulator', WINDOW_HEIGHT / 2, (0, 0, 0), (255, 0, 0), 48)
    MenuButton(button_groups, 1002, 'Settings', WINDOW_HEIGHT / 2 + 80, (0, 0, 0), (255, 0, 0), 48)
  
  def create_bg(self, groups: list):
    SimBG(groups)
  
  def create_sun(self, groups: list, sun_pos: tuple, sun_mass: int):
    Sun(groups, 25, sun_pos, sun_mass)

  def create_traildots(self, groups: list, satellites, trail_sprites):
    TrailDots().draw_trails(groups, satellites, trail_sprites)

class SimBG(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)

    # surface
    self.image = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    self.rect = self.image.get_rect(topleft = (0, 0))

    # background image
    bg_img = pygame.image.load('assets/graphics/sim/bg.jpg').convert()
    bg_scale_factor = WINDOW_HEIGHT / bg_img.get_height()
    full_width = bg_img.get_width() * bg_scale_factor
    full_height = bg_img.get_height() * bg_scale_factor
    scaled_bg_img = pygame.transform.scale(bg_img, (full_width, full_height))
    bg_rect = scaled_bg_img.get_rect(topleft = (0, 0))
    self.image.blit(scaled_bg_img, bg_rect)

    # grid line
    self.draw_gridlines(self.image)

  def draw_gridlines(self, display_surface):
    grid_color = (100, 150, 100)
    grid_size = 50 # size of each square in pixels
    grid_cells = pygame.math.Vector2((round(WINDOW_WIDTH / grid_size), round(WINDOW_HEIGHT / grid_size))) # number of grid cells that fit in the window in each dimension
    center_line_width = 3
    center_x = round(WINDOW_WIDTH / 2)
    center_y = round(WINDOW_HEIGHT / 2)

    def draw_cell_lines(grid_cells_vect, line_width, cell_selector):
      for cell in range(0, round(grid_cells_vect.x) + 1):
        right_x = center_x + (cell * (grid_size * cell_selector))
        left_x = center_x - (cell * (grid_size * cell_selector))
        pygame.draw.line(display_surface, grid_color, (right_x, 0), (right_x, WINDOW_HEIGHT), line_width)
        pygame.draw.line(display_surface, grid_color, (left_x, 0), (left_x, WINDOW_HEIGHT), line_width)
      
      for cell in range(0, round(grid_cells_vect.y) + 1):
        right_y = center_y + (cell * (grid_size * cell_selector))
        left_y = center_y - (cell * (grid_size * cell_selector))
        pygame.draw.line(display_surface, grid_color, (0, right_y), (WINDOW_WIDTH, right_y), line_width)
        pygame.draw.line(display_surface, grid_color, (0, left_y), (WINDOW_WIDTH, left_y), line_width)

    # Draw central lines
    pygame.draw.line(display_surface, grid_color, (center_x, 0), (center_x, WINDOW_HEIGHT), center_line_width)
    pygame.draw.line(display_surface, grid_color, (0, center_y), (WINDOW_WIDTH, center_y), center_line_width)

    # Draw every fifth line
    draw_cell_lines(grid_cells, 2, 5)

    # Draw grid lines
    draw_cell_lines(grid_cells, 1, 1)

class Sun(pygame.sprite.Sprite):
  def __init__(self, groups, size, pos, mass):
    super().__init__(groups)
    self.size = size
    self.mass = mass
    scale_factor = self.size / pygame.image.load('assets/graphics/sim/sun1.png').get_height()
    
    surf = pygame.image.load('assets/graphics/sim/sun1.png').convert_alpha()
    self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)

    self.rect = self.image.get_rect(center = pos)
    self.pos = pygame.math.Vector2(self.rect.center)

    self.mask = pygame.mask.from_surface(self.image)

class Satellite(pygame.sprite.Sprite):
  def __init__(self, groups, pos, speed, color, sun_sprites):
    super().__init__(groups)
    self.sim_slowdown = 10
    self.color = color
    self.size = 10
    self.init_position = pos
    self.speed = pygame.math.Vector2(speed)
    self.sun_sprites = sun_sprites

    self.image = pygame.surface.Surface((self.size, self.size))
    self.image.fill((255, 0, 255))
    self.image.set_colorkey((255, 0, 255))

    self.rect = self.image.get_rect(center = self.init_position)
    self.pos = pygame.math.Vector2(self.rect.center)
    self.mask = pygame.mask.from_surface(self.image)

    pygame.draw.circle(self.image, self.color, (self.size / 2, self.size / 2), self.size / 2)

    # math calcs
    self.piovertwo = math.pi / 2
    self.pi = math.pi
    self.threepiovertwo = (3 * math.pi) / 2

  def update(self):
    # for sun_sprite in self.sun_sprites:
    #   gravitational_force = Physics().gravitational_force(sun_sprite.mass, sun_sprite.pos, self.pos)
    #   print(gravitational_force)
    #   self.speed -= gravitational_force

    sun_mass = 750
    sun_pos = (400, 400)
    gravitational_force = Physics().gravitational_force(sun_mass, sun_pos, self.pos)
    self.speed -= gravitational_force

    # calc new position
    self.pos += self.speed
    self.rect.center = pygame.math.Vector2((round(self.pos.x), round(self.pos.y)))

class TrailDots():
  def __init__(self):
    pass

  def draw_trails(self, group_list, satellites_group, trail_sprites_group):
    for sprite in satellites_group:
      self.TrailDot(group_list, sprite.color, sprite.pos)
    
    for sprite in trail_sprites_group:
      seconds = 10
      frames = seconds * FRAMERATE
      sprite.timer += 1
      if sprite.timer > frames:
        sprite.kill()

  class TrailDot(pygame.sprite.Sprite):
    def __init__(self, groups, color, pos):
      super().__init__(groups)
      self.pos = pygame.math.Vector2((round(pos.x), round(pos.y)))
      self.timer = 0

      self.image = pygame.surface.Surface((2, 2))
      self.rect = self.image.get_rect(center = pos)

      pygame.draw.circle(self.image, color, (1, 1), 1)

class MenuBG(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)

    surf = pygame.image.load('assets/graphics/menu/bg.jpg')
    scale_factor = WINDOW_HEIGHT / surf.get_height()
    self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
    self.rect = self.image.get_rect(topleft = (0, 0))

class MenuButton(pygame.sprite.Sprite):
  def __init__(self, groups, id: int, text: str, y_pos: int, bg_color: tuple, font_color: tuple, font_size: int):
    super().__init__(groups)
    self.id = id
    self.text = text
    self.font_color = font_color
    self.size = (400, 60)
    self.hover = False

    self.button_font = pygame.font.Font('assets/fonts/Pixeltype.ttf', font_size)
    
    self.image = pygame.surface.Surface(self.size)
    self.image.fill(bg_color)
    self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH / 2, y_pos))

  def update(self):
    # update text to surface
    text_surf = self.button_font.render(self.text, True, self.font_color)
    text_rect = text_surf.get_rect(midtop = (self.size[0] / 2, 16))
    self.image.blit(text_surf, text_rect)