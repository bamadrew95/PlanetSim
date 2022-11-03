from turtle import window_height
import pygame
from settings import *
from game_files.physics import Physics
import math
from random import randint

class CreateSprites:
  def __init__(self):
    pass

  def init_sim(self, bg_groups: list, sun_groups: list, sun_pos: tuple, sun_mass: int):
    self.bg(bg_groups)
    self.sun(sun_groups, sun_pos, sun_mass)       
    
  def main_menu(self, bg_groups: list, button_groups: list):
    MenuBG(bg_groups)
    MenuButton(button_groups, 1001, 'Start Simulator', WINDOW_HEIGHT / 2, (0, 0, 0), (255, 0, 0), 48)
    MenuButton(button_groups, 1002, 'Settings', WINDOW_HEIGHT / 2 + 80, (0, 0, 0), (255, 0, 0), 48)

  def settings_menu(self, bg_groups: list, slider_groups: list):
    MenuBG(bg_groups)
    self.volume_setting = MenuSlider(slider_groups, 1101, 'Music Volume', 0)
    # self.volume_setting = MenuSlider(slider_groups, 1102, 'Game Speed', 1)
    # self.volume_setting = MenuSlider(slider_groups, 1103, 'Test', 2)
    # MenuSlider(slider_groups, 1101, 'Volume', (WINDOW_HEIGHT / 2) - 100)
  
  def bg(self, groups: list):
    SimBG(groups)
  
  def sun(self, groups: list, sun_pos: tuple, sun_mass: int):
    Sun(groups, 25, sun_pos, sun_mass)
  
  def satellite(self, groups: list, pos: tuple, speed: tuple, color: tuple, sun_sprites):
    Satellite(groups, pos, speed, color, sun_sprites)

  def traildots(self, groups: list, satellites, trail_sprites):
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
    for sun_sprite in self.sun_sprites:
      gravitational_force = Physics().gravitational_force(sun_sprite.mass, sun_sprite.pos, self.pos)
      self.speed -= gravitational_force

    # calc new position
    self.pos += self.speed
    self.rect.center = pygame.math.Vector2((round(self.pos.x), round(self.pos.y)))

class TrailDots():
  def __init__(self):
    pass

  def draw_trails(self, group_list, satellites_group, trail_sprites_group):
    x =+ 1
    for sprite in satellites_group:
      if (x // 2) == 0:
        self.TrailDot(group_list, sprite.color, sprite.pos)
    
    if x > 64:
      x = 0
    
    for sprite in trail_sprites_group:
      seconds = 10
      frames = seconds * FRAMERATE
      sprite.timer += 1
      if sprite.timer > frames:
        sprite.kill()
        del sprite

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
    self.bg_color = bg_color
    self.font_color = font_color
    self.size = (400, 60)
    self.hover = False

    self.button_font = pygame.font.Font('assets/fonts/Pixeltype.ttf', font_size)
    
    self.image = pygame.surface.Surface(self.size)
    self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH / 2, y_pos))

  def update(self):
    # update text to surface
    self.image.fill(self.bg_color)
    text_surf = self.button_font.render(self.text, False, self.font_color)
    text_rect = text_surf.get_rect(midtop = (self.size[0] / 2, 16))
    self.image.blit(text_surf, text_rect)

class MenuSlider(pygame.sprite.Sprite):
  def __init__(self, groups, id: int, label: str, setting_index: int):
    super().__init__(groups)
    self.id = id
    self.value = MUSIC_VOLUME
    self.label = label
    self.setting_index = setting_index
    self.label_text = self.label + ': ' + str(self.value)
    self.size = (400, 80)
    box_y_pos = (WINDOW_HEIGHT / 3) + (setting_index * self.size[1] * 1.1)

    # slider box
    self.bg_color = (25, 25, 25)
    self.image = pygame.surface.Surface(self.size)
    self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH / 2, box_y_pos))

    # label
    font_size = 32
    self.font_color = (255, 0, 0)
    self.font = pygame.font.Font('assets/fonts/Pixeltype.ttf', font_size)
    font_surf = self.font.render(self.label_text, False, self.font_color)
    self.font_rect = font_surf.get_rect(topleft = (10, 10))
    self.image.blit(font_surf, self.font_rect)

    # slider track
    self.track_color = (50, 50, 50)
    self.margin = 20
    self.track_y = 60

    # slider handle
    handle_color = (150, 150, 150)
    handle_size = 30
    init_handle_x_pos = (self.value / 100) * (self.size[0] - self.margin * 2)
    self.handle_surf = pygame.surface.Surface((handle_size, handle_size))
    self.handle_rect = self.handle_surf.get_rect(center = (init_handle_x_pos, self.track_y))
    self.handle_surf.set_colorkey((255, 0, 255))
    self.handle_surf.fill((255, 0, 255))
    pygame.draw.circle(self.handle_surf, handle_color, (handle_size / 2, handle_size / 2), handle_size / 2)

  def update(self):
    mouse_pos = pygame.mouse.get_pos()

    # refill bg
    self.image.fill(self.bg_color)

    if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
      self.value = self.change_value(mouse_pos[0])
    
    # render text
    self.label_text = self.label + ': ' + str(self.value)
    font_surf = self.font.render(self.label_text, False, self.font_color)
    self.image.blit(font_surf, self.font_rect)

    # render track
    pygame.draw.line(self.image, self.track_color, (self.margin, self.track_y), (self.size[0] - self.margin, self.track_y), 4)

    # render slider handle
    x = self.value / 100 * (self.size[0] - self.margin * 2) + self.margin
    self.handle_rect.centerx = x
    self.image.blit(self.handle_surf, self.handle_rect)

  def change_value(self, x_pos: int) -> int:
    value = x_pos - ((WINDOW_WIDTH - (self.size[0] - (self.margin * 2))) / 2)
    value = round(value / (self.size[0] - self.margin * 2) * 100)
    if value < 0:
      value = 0
    elif value > 100:
      value = 100
    return value