import pygame
from settings import *
from game_files.physics import Physics
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
    sun_mass = 750
    sun_pos = pygame.math.Vector2((400, 400))
    gravitational_force = Physics().gravitational_force(sun_mass, sun_pos, self.pos)

    self.speed -= gravitational_force

    # calc new position
    self.pos += self.speed
    self.rect.center = pygame.math.Vector2((round(self.pos.x), round(self.pos.y)))

class TrailDot(pygame.sprite.Sprite):
  def __init__(self, groups, color, pos):
    super().__init__(groups)
    self.pos = pygame.math.Vector2((round(pos.x), round(pos.y)))
    self.timer = 0

    self.image = pygame.surface.Surface((2, 2))
    self.rect = self.image.get_rect(center = pos)

    pygame.draw.circle(self.image, color, (1, 1), 1)

class Arrow(pygame.sprite.Sprite):
  def __init__(self, groups, color, start_pos):
    super().__init__(groups)

    magenta = (255, 0, 255)

    self.image = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    self.image.fill((255, 0, 255))
    self.image.set_colorkey(magenta)
    self.rect = self.image.get_rect(topleft = (0, 0))

    pygame.draw.line(self.image, color, start_pos, pygame.mouse.get_pos(), 4)
    