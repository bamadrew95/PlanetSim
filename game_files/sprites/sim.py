import pygame
from settings import *
from documentation import *
from game_files.physics import Physics
import math

class CreateSimSprites:
  def __init__(self):
    pass

  def init_sim(self, bg_groups: list, grid_size: int, sun_groups: list, sun_pos: tuple, sun_mass: int):
    self.SimBG(bg_groups, grid_size)
    self.Sun(sun_groups, 50, sun_pos, sun_mass)

  def traildots(self, groups: list, satellites, trail_sprites, trail_longevity, dt):
    self.TrailDots().draw_trails(groups, satellites, trail_sprites, trail_longevity, dt)

  class SimBG(pygame.sprite.Sprite):
    def __init__(self, groups: PygameSpriteGroupList, grid_size: int):
      super().__init__(groups)
      self.grid_size = grid_size
      self.grid_color = (50, 100, 50)

      # surface
      self.image = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
      self.rect = self.image.get_rect(topleft = (0, 0))

      # background image
      bg_img = pygame.image.load('assets/graphics/sim/bg.jpg').convert()
      bg_scale_factor = WINDOW_HEIGHT / bg_img.get_height()
      full_width = bg_img.get_width() * bg_scale_factor
      full_height = bg_img.get_height() * bg_scale_factor
      self.scaled_bg_img = pygame.transform.scale(bg_img, (full_width, full_height))
      self.bg_rect = self.scaled_bg_img.get_rect(topleft = (0, 0))

    def update(self, dt):
      self.image.blit(self.scaled_bg_img, self.bg_rect)
      self._draw_gridlines()

    def _draw_gridlines(self):
      halfscreen = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
      grid_cells = round(halfscreen[0] / self.grid_size), round(halfscreen[1] / self.grid_size) # number of grid cells that fit in the window in each dimension
      center_line_width = 6
      subgrid_width = 3
      grid_width = 1

      # Draw Center Lines
      pygame.draw.line(self.image, self.grid_color, (0, halfscreen[1]), (WINDOW_WIDTH, halfscreen[1]), center_line_width)
      pygame.draw.line(self.image, self.grid_color, (halfscreen[0], 0), (halfscreen[0], WINDOW_HEIGHT), center_line_width)

      for cell in range(1, grid_cells[0] + 1):
        if not (cell) % 5:
          # Draw Subgrid
            # Horizontal lines
          pygame.draw.line(self.image, self.grid_color, (0, halfscreen[1] + self.grid_size * cell), (WINDOW_WIDTH, halfscreen[1] + self.grid_size * cell), subgrid_width)
          pygame.draw.line(self.image, self.grid_color, (0, halfscreen[1] - self.grid_size * cell), (WINDOW_WIDTH, halfscreen[1] - self.grid_size * cell), subgrid_width)
            # Vertical lines
          pygame.draw.line(self.image, self.grid_color, (halfscreen[0] + self.grid_size * cell, 0), (halfscreen[0] + self.grid_size * cell, WINDOW_HEIGHT), subgrid_width)
          pygame.draw.line(self.image, self.grid_color, (halfscreen[0] - self.grid_size * cell, 0), (halfscreen[0] - self.grid_size * cell, WINDOW_HEIGHT), subgrid_width)
        else:
          # Draw regular grid lines
            # Horizontal lines
          pygame.draw.line(self.image, self.grid_color, (0, halfscreen[1] + self.grid_size * cell), (WINDOW_WIDTH, halfscreen[1] + self.grid_size * cell), grid_width)
          pygame.draw.line(self.image, self.grid_color, (0, halfscreen[1] - self.grid_size * cell), (WINDOW_WIDTH, halfscreen[1] - self.grid_size * cell), grid_width)
            # Vertical lines
          pygame.draw.line(self.image, self.grid_color, (halfscreen[0] + self.grid_size * cell, 0), (halfscreen[0] + self.grid_size * cell, WINDOW_HEIGHT), grid_width)
          pygame.draw.line(self.image, self.grid_color, (halfscreen[0] - self.grid_size * cell, 0), (halfscreen[0] - self.grid_size * cell, WINDOW_HEIGHT), grid_width)

  class Sun(pygame.sprite.Sprite):
    def __init__(self, groups: PygameSpriteGroupList, size: int, pos: tuple, mass: int):
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
    def __init__(self, groups: PygameSpriteGroupList, pos: tuple, speed: tuple, color: TripleTuple, sun_sprites: PygameSpriteGroupList):
      super().__init__(groups)
      self.sim_slowdown = 10
      self.color = color
      self.size = 10
      self.init_position = pos
      self.speed = pygame.math.Vector2(speed)
      self.sun_sprites = sun_sprites
      self.timer = 0

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

    def update(self, dt: float):
      for sun_sprite in self.sun_sprites:
        gravitational_force = Physics().gravitational_force(sun_sprite.mass, sun_sprite.pos, self.pos)
        self.speed -= gravitational_force * dt

      # calc new position
      self.pos += self.speed * dt
      self.rect.center = pygame.math.Vector2((round(self.pos.x), round(self.pos.y)))

      if math.sqrt(math.pow(self.pos.x, 2) + math.pow(self.pos.y, 2)) > 5000:
        self.kill()
        del self

  class TrailDots():
    def __init__(self):
      pass

    def draw_trails(self, group_list: PygameSpriteGroupList, satellites_group: PygameSpriteGroupList, trail_sprites_group: PygameSpriteGroupList, trail_longevity: int, dt: float):
      for sprite in satellites_group:
        if sprite.timer > 2:
          self.TrailDot(group_list, sprite.color, sprite.pos)
          sprite.timer = 0
        sprite.timer += 1 * dt
      
      for sprite in trail_sprites_group:
        seconds = trail_longevity
        frames = seconds * FRAMERATE
        sprite.timer += 1
        if sprite.timer > frames:
          sprite.kill()
          del sprite

    class TrailDot(pygame.sprite.Sprite):
      def __init__(self, groups: PygameSpriteGroupList, color: TripleTuple, pos: tuple):
        super().__init__(groups)
        self.pos = pygame.math.Vector2((round(pos.x), round(pos.y)))
        self.timer = 0

        self.image = pygame.surface.Surface((2, 2))
        self.rect = self.image.get_rect(center = pos)

        pygame.draw.circle(self.image, color, (1, 1), 1)
