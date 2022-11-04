import pygame
from settings import *
from documentation import *
from game_files.sprites.sim import CreateSimSprites
from game_files.physics import Physics
import math

class UI():
  def __init__(self):
    self.create_sprites = CreateSimSprites()
    
  def create_main_menu(self, bg_groups: PygameSpriteGroupList, button_groups: PygameSpriteGroupList):
    self.MenuBG(bg_groups)
    self.TextBanner(bg_groups, 'Planet Simulator', (WINDOW_WIDTH / 1.5, 100), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 10), (25, 25,25), (255, 0, 0), 72)
    self.MenuButton(button_groups, 1001, 'Start Simulator', (400, 60), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), (25, 25, 25), (255, 0, 0), (0, 255, 0), 48)
    self.MenuButton(button_groups, 1002, 'Settings', (400, 60), (WINDOW_WIDTH / 2 ,WINDOW_HEIGHT / 2 + 80), (25, 25, 25), (255, 0, 0), (0, 255, 0), 48)
    self.MenuButton(button_groups, 1099, 'Quit', (400, 60), (WINDOW_WIDTH / 2 ,WINDOW_HEIGHT / 2 + 160), (25, 25, 25), (255, 0, 0), (0, 255, 0), 48)

  def create_quitmenu(self, bg_groups: PygameSpriteGroupList, button_groups: PygameSpriteGroupList):
    self.MenuBG(bg_groups)
    self.TextBanner(bg_groups, 'Are you sure you want to quit?', (WINDOW_WIDTH / 1.5, 150), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3), (25, 25, 25), (255, 0, 0), 48)
    self.MenuButton(button_groups, 9001, 'Yes', (300, 75), (WINDOW_WIDTH / 2 - 160, WINDOW_HEIGHT / 3 * 2), (25, 25, 25), (255, 0, 0), (0, 255, 0), 48)
    self.MenuButton(button_groups, 9002, 'No', (300, 75), (WINDOW_WIDTH / 2 + 160, WINDOW_HEIGHT / 3 * 2), (25, 25, 25), (255, 0, 0), (0, 255, 0), 48)

  def create_settings_menu(self, bg_groups: PygameSpriteGroupList, slider_groups: PygameSpriteGroupList, button_groups: PygameSpriteGroupList):
    self.MenuBG(bg_groups)
    self.TextBanner(bg_groups, 'Settings', (600, 75), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 12), (25, 25, 25), (255, 0, 0), 64)
    self.MenuSlider(slider_groups, 1100, 'Game Speed', 1, 10, GAME_SPEED, 0)
    self.MenuSlider(slider_groups, 1101, 'Trail Length', 0, 60, TRAIL_LENGTH, 1)
    self.MenuSlider(slider_groups, 1105, 'Grid Size', 10, 200, GRIDSIZE, 2)
    self.MenuSlider(slider_groups, 1102, 'Music Volume', 0, 100, MUSIC_VOLUME, 3)
    self.MenuSlider(slider_groups, 1103, 'Effects Volume', 0, 100, EFFECTS_VOLUME, 4)
    self.MenuSlider(slider_groups, 1104, 'Max Framerate', 30, 120, FRAMERATE, 5)
    self.MenuButton(button_groups, 1198, 'Reset to Defaults', (250, 50), (WINDOW_WIDTH / 2 + 135, WINDOW_HEIGHT - 25), (25, 25, 25), (255, 0, 0), (0, 255, 0), 32)
    self.MenuButton(button_groups, 1199, 'Back', (250, 50), (WINDOW_WIDTH / 2 - 135, WINDOW_HEIGHT - 25), (25, 25, 25), (255, 0, 0), (0, 255, 0), 32)

  def get_slider_setting(self, slider_sprites: PygameSpriteGroupList, slider_id: int) -> int:
    for slider in slider_sprites:
      if slider.id == slider_id:
        return slider.value

  def detect_hover(self, sprite_group: PygameSpriteGroupList, default_cursor: PygameCursor, pointer_cursor: PygameCursor):
    hover = 0
    for sprite in sprite_group:
      if sprite.rect.collidepoint(pygame.mouse.get_pos()):
        sprite.hover = True
        hover += 1
      else:
        sprite.hover = False

    if hover:
      pygame.mouse.set_cursor(pointer_cursor)
    else:
      pygame.mouse.set_cursor(default_cursor)

  def add_mode(self, surface: DisplaySurface, click_pos: tuple, font: PygameFont, color: TripleTuple):
    line_width = 4
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.line(surface, color, click_pos, mouse_pos, line_width)

    self.velocity_meter = self.VelocityMeter(surface, click_pos, mouse_pos, font, color)

    return self.velocity_meter.velocity

  class MenuBG(pygame.sprite.Sprite):
    def __init__(self, groups: PygameSpriteGroupList):
      super().__init__(groups)

      surf = pygame.image.load('assets/graphics/menu/bg.jpg')
      scale_factor = WINDOW_HEIGHT / surf.get_height()
      self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
      self.rect = self.image.get_rect(topleft = (0, 0))

  class MenuButton(pygame.sprite.Sprite):
    def __init__(self, groups: PygameSpriteGroupList, id: int, text: str, size: tuple, pos: tuple, bg_color: TripleTuple, font_color: TripleTuple, font_hover_color: TripleTuple, font_size: int):
      super().__init__(groups)
      self.id = id
      self.text = text
      self.bg_color = bg_color
      self.font_color = font_color
      self.font_hover_color = font_hover_color
      self.size = size
      self.hover = False

      self.button_font = pygame.font.Font('assets/fonts/Pixeltype.ttf', font_size)
      
      self.image = pygame.surface.Surface(self.size)
      self.rect = self.image.get_rect(midbottom = pos)

    def update(self, dt):
      if self.hover:
        color = self.font_hover_color
      else:
        color = self.font_color

      # update text to surface
      self.image.fill(self.bg_color)
      text_surf = self.button_font.render(self.text, False, color)
      text_rect = text_surf.get_rect(center = (self.size[0] / 2, self.size[1] / 2))
      self.image.blit(text_surf, text_rect)

  class MenuSlider(pygame.sprite.Sprite):
    def __init__(self, groups: PygameSpriteGroupList, id: int, label: str, min_value: int, max_value: int, init_value: int, setting_index: int):
      super().__init__(groups)
      self.id = id
      self.label = label
      self.min_value = min_value
      self.max_value = max_value
      self.value = init_value
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
      init_handle_x_pos = (self.value - self.min_value) * ((self.size[0] - (self.margin * 2)) / (self.max_value - self.min_value)) + self.margin
      self.handle_surf = pygame.surface.Surface((handle_size, handle_size))
      self.handle_rect = self.handle_surf.get_rect(center = (init_handle_x_pos, self.track_y))
      self.handle_surf.set_colorkey((255, 0, 255))
      self.handle_surf.fill((255, 0, 255))
      pygame.draw.circle(self.handle_surf, handle_color, (handle_size / 2, handle_size / 2), handle_size / 2)

    def update(self, dt: float):
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
      x = (self.value - self.min_value) * ((self.size[0] - (self.margin * 2)) / (self.max_value - self.min_value)) + self.margin
      self.handle_rect.centerx = x
      self.image.blit(self.handle_surf, self.handle_rect)

    def change_value(self, x_pos: int) -> int:
      value = round(((x_pos - ((WINDOW_WIDTH - (self.size[0] - self.margin * 2)) / 2)) * (1 / (self.size[0] - self.margin * 2)) * (self.max_value - self.min_value)) + self.min_value)
      if value < self.min_value:
        value = self.min_value
      elif value > self.max_value:
        value = self.max_value
      return value

  class TextBanner(pygame.sprite.Sprite):
    def __init__(self, groups: PygameSpriteGroupList, text: str, size: tuple, pos: tuple, bg_color: TripleTuple, font_color: TripleTuple, font_size):
      super().__init__(groups)
      self.text = text
      self.size = size
      self.pos = pos
      self.bg_color = bg_color
      self.font_size = font_size
      self.font_color = font_color

      # BG
      self.image = pygame.surface.Surface(self.size)
      self.image.fill(bg_color)
      self.rect = self.image.get_rect(midtop = pos)

      # Text
      self.font = pygame.font.Font('assets/fonts/Pixeltype.ttf', self.font_size)
      self.font_surf = self.font.render(self.text, False, font_color)
      self.font_rect = self.font_surf.get_rect(center = (self.size[0] / 2, self.size[1] / 2))
      self.image.blit(self.font_surf, self.font_rect)
  
  class VelocityMeter:
    def __init__(self, surface: DisplaySurface, click_pos: tuple, mouse_pos: tuple, font: PygameFont, color: TripleTuple):
      self.screen = surface
      self.click_pos = pygame.math.Vector2(click_pos)
      self.mouse_pos = pygame.math.Vector2(mouse_pos)
      self.font = font
      self.color = color

      rel_vect = self.click_pos - self.mouse_pos
      distance_tuple = (abs(rel_vect.x), abs(rel_vect.y))

      distance = math.sqrt(math.pow(rel_vect.x, 2) + math.pow(rel_vect.y, 2))
      self.total_velocity = round(math.pow(distance / 100, 2), 2)

      force = distance / 50 # 50 comes from default grid size. I decided not to make it change with the grid size setting.
      theta = Physics().find_angle((rel_vect.x, rel_vect.y), distance_tuple)
      force_x = force * math.cos(theta)
      force_y = force * math.sin(theta)
      self.velocity = (-force_x, force_y)

      surf = self.font.render(str(round(force, 2)), False, color)

      if mouse_pos[0] >= click_pos[0]:
        rect = surf.get_rect(midright = (click_pos[0] - 10, click_pos[1]))
      else:
        rect = surf.get_rect(midleft = (click_pos[0] + 10, click_pos[1]))

      self.screen.blit(surf, rect)
