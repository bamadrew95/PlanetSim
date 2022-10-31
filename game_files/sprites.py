import pygame
from settings import *
import math

class BG(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)

    # surface
    self.image = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    self.rect = self.image.get_rect(topleft = (0, 0))

    # background image
    bg_img = pygame.image.load('assets/graphics/sim/bg1.jpg').convert()
    bg_scale_factor = WINDOW_WIDTH / bg_img.get_height()
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
  def __init__(self, groups, size):
    super().__init__(groups)
    self.size = size
    color = (255, 255, 200)
    initial_position = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    self.mass = 8

    self.image = pygame.surface.Surface((self.size, self.size))
    self.image.set_colorkey((255, 0, 255))
    self.image.fill((255, 0, 255))
    pygame.draw.circle(self.image, color, (self.size / 2, self.size / 2), self.size / 2)

    self.rect = self.image.get_rect(center = initial_position)
    self.pos = pygame.math.Vector2(self.rect.center)
    self.mask = pygame.mask.from_surface(self.image)

class Satellite(pygame.sprite.Sprite):
  def __init__(self, groups, pos, speed, color):
    super().__init__(groups)
    self.sim_slowdown = 10
    self.color = color
    self.size = 10
    self.init_position = pos
    self.speed = pygame.math.Vector2(speed)

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
    sun_mass = 8
    sun_pos = pygame.math.Vector2((400, 400))
    # self.pos = pygame.math.Vector2(pygame.mouse.get_pos())

    rel_pos = self.pos - sun_pos
    rel_pos.y = -rel_pos.y

    distance_vect = pygame.math.Vector2((abs(rel_pos.x), abs(rel_pos.y)))

    distance = math.sqrt(math.pow(rel_pos.x, 2) + math.pow(rel_pos.y, 2))

    # calc gravitational strength
    if distance and distance < 400:
      gravity_force = sun_mass / math.pow(distance, 2)
    else:
      gravity_force = 0

    # find quadrant
    if rel_pos.x >= 0 and rel_pos.y < 0:
      quad = 1
    elif rel_pos.x < 0 and rel_pos.y < 0:
      quad = 2
    elif rel_pos.x < 0 and rel_pos.y >= 0:
      quad = 3
    else:
      quad = 4

    # calc theta
    if quad == 1:
      if distance_vect.x:
        theta = math.atan(distance_vect.y / distance_vect.x)
      else:
        theta = self.piovertwo

    if quad == 2:
      if distance_vect.y:
        theta = (math.atan(distance_vect.x / distance_vect.y)) + (self.piovertwo)
      else:
        theta = self.pi
    
    if quad == 3:
      if distance_vect.x:
        theta = (math.atan(distance_vect.y / distance_vect.x)) + (self.pi)
      else:
        theta = self.threepiovertwo / 2

    if quad == 4:
      if distance_vect.y:
        theta = (math.atan(distance_vect.x / distance_vect.y)) + (self.threepiovertwo)
      else:
        theta = 0

    # calc change in speed
    gravitational_force = pygame.math.Vector2((math.cos(theta) / self.sim_slowdown, math.sin(theta) / self.sim_slowdown))
    self.speed -= gravitational_force

    # calc new position
    self.pos += self.speed
    self.rect.center = pygame.math.Vector2((round(self.pos.x), round(self.pos.y)))

class TrailDot(pygame.sprite.Sprite):
  def __init__(self, groups, color, pos):
    super().__init__(groups)
    self.pos = pygame.math.Vector2((round(pos.x), round(pos.y)))
    self.time = 0

    self.image = pygame.surface.Surface((2, 2))
    self.rect = self.image.get_rect(center = pos)

    pygame.draw.circle(self.image, color, (1, 1), 1)