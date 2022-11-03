import pygame
from settings import *
from game_files.sprites.sim import CreateSprites, MenuButton
import math

Function = object

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

  class DialogueBox(pygame.sprite.Sprite):
    def __init__(self, dialogue_box_groups: list, button_groups: list, label: str, option1: str, option2: str, func: Function):
      super().__init__(dialogue_box_groups)
      self.button_groups = button_groups
      self.label = label
      self.option1 = option1
      self.option2 = option2
      self.func = func
      self.size = (600, 400)
      
      # bg
      bg_color = (50, 50, 50)
      self.image = pygame.surface.Surface(self.size)
      self.image.fill(bg_color)
      self.rect = self.image.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

      # text
      self.font_size = 48
      self.font_color = (255, 0, 0)
      self.font = pygame.font.Font('assets/fonts/Pixeltype.ttf', self.font_size)
      font_surf = self.font.render(label, False, self.font_color)
      font_rect = font_surf.get_rect(center = (self.size[0] / 2, self.size[1] / 4))
      self.image.blit(font_surf, font_rect)

      # yes button
      button_size = (250, 75)
      self.add_button('Yes', 9001, button_size, (self.rect.centerx - (button_size[0] / 2 + 15), self.rect.centery + 150))
      self.add_button('No', 9002, button_size, (self.rect.centerx + (button_size[0] / 2 + 15), self.rect.centery + 150))

    def run(self):
      self.func()

    def add_button(self, text, id, size, pos):
      MenuButton(self.button_groups, id, text, size, pos, (0, 0, 0), self.font_color, self.font_size)