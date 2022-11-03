import pygame
from settings import *
from game_files.sprites import CreateSprites
import math

class UI():
  def __init__(self):
    self.create_sprites = CreateSprites()
    
  def create_main_menu(self, bg_groups, button_groups):
    self.create_sprites.main_menu(bg_groups, button_groups)

  def create_settings_menu(self, bg_groups, slider_groups):
    self.create_sprites.settings_menu(bg_groups, slider_groups)

  def get_slider_setting(self, slider_sprites, slider_id: int) -> int:
    for slider in slider_sprites:
      if slider.id == slider_id:
        return slider.value

  def detect_hover(self, sprite_group, default_cursor, pointer_cursor):
    hover = 0
    for sprite in sprite_group:
      if hasattr(sprite, 'handle_rect'):
        if sprite.handle_rect.collidepoint(pygame.mouse.get_pos()):
          sprite.hover = True
          hover += 1
        else:
          sprite.hover = False
      else:
        if sprite.rect.collidepoint(pygame.mouse.get_pos()):
          sprite.hover = True
          hover += 1
        else:
          sprite.hover = False

    if hover:
      pygame.mouse.set_cursor(pointer_cursor)
    else:
      pygame.mouse.set_cursor(default_cursor)

  def add_mode(self, surface, click_pos, font, color):
    line_width = 4
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.line(surface, color, click_pos, mouse_pos, line_width)

    self.velocity_meter = self.VelocityMeter(surface, click_pos, mouse_pos, font, color)

    return self.velocity_meter.velocity

  def add_satellite(self, group_list, init_pos, velocity, color, orbiting_sprites):
    self.create_sprites.satellite(group_list, init_pos, velocity, color, orbiting_sprites)

  class VelocityMeter:
    def __init__(self, surface, click_pos, mouse_pos, font, color):
      self.screen = surface
      self.click_pos = pygame.math.Vector2(click_pos)
      self.mouse_pos = pygame.math.Vector2(mouse_pos)
      self.font = font
      self.color = color

      rel_vect = self.click_pos - self.mouse_pos

      distance = math.sqrt(math.pow(rel_vect.x, 2) + math.pow(rel_vect.y, 2))
      self.total_velocity = round(math.pow(distance / 100, 2), 2)

      if rel_vect.x < 0:
        rel_vect.x = math.pow(rel_vect.x / 100, 2)
      else:
        rel_vect.x = -math.pow(rel_vect.x / 100, 2)

      if rel_vect.y < 0:
        rel_vect.y = math.pow(rel_vect.y / 100, 2)
      else:
        rel_vect.y = -math.pow(rel_vect.y / 100, 2)

      self.velocity = (rel_vect.x, rel_vect.y)

      surf = self.font.render(str(self.total_velocity), False, color)

      if mouse_pos[0] >= click_pos[0]:
        rect = surf.get_rect(midright = (click_pos[0] - 10, click_pos[1]))
      else:
        rect = surf.get_rect(midleft = (click_pos[0] + 10, click_pos[1]))

      self.screen.blit(surf, rect)
