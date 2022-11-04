import pygame, sys
from settings import *
from game_files.sprites.sim import CreateSimSprites
from game_files.sprites.ui import UI
from game_files.physics import Physics
from game_files.audio import Sound
from random import randint

class Game():
  def __init__(self): 
    self.import_settings()
    self.init_pygame()
    self.create_cursors()
    self.create_fonts()
    self.set_initial_states()
    self.run_game_files()
    self.audio_config()
    self.create_sprite_groups()
    self.create_sprites()
  
  def import_settings(self):
    # import settings
    self.window_width = WINDOW_WIDTH
    self.window_height = WINDOW_HEIGHT
    self.framerate = FRAMERATE
    self.game_state = INITIAL_GAME_STATE
    self.game_speed = GAME_SPEED
    self.trail_length = TRAIL_LENGTH
    self.grid_size = GRIDSIZE
    self.music_volume = MUSIC_VOLUME
    self.effects_volume = EFFECTS_VOLUME

  def init_pygame(self):
    # Initialization of pygame window
    pygame.init()
    self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.NOFRAME)
    pygame.display.set_caption('Planet Simulator')
    self.clock = pygame.time.Clock()

  def create_cursors(self):
    # Cursors
    self.default_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
    self.pointer_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
    pygame.mouse.set_cursor(self.default_cursor)
  
  def create_fonts(self):
    # Fonts
    self.default_font = pygame.font.Font('assets/fonts/Pixeltype.ttf', 24)
  
  def set_initial_states(self):
    # initial states
    self.paused = False
    self.click_pos = (0, 0)
    self.add_mode = False
    self.velocity_selector = (0, 0)
  
  def run_game_files(self):
    # run game_files
    self.ui = UI()
    self.physics = Physics()
  
  def audio_config(self):
    # AUDIO
      # music
    self.menu_music = Sound('Acadia.mp3', self.music_volume)
    self.sim_music = Sound('DreamyFlashback.mp3', self.music_volume)
    self.paused_music = Sound('FrozenStar.mp3', self.music_volume)
    self.menu_music.play_loop()
      # sound effects
    self.crash_sound = Sound('impact.mp3', self.effects_volume)
  
  def create_sprite_groups(self):
    # SPRITE GROUPS
    self.all_sprites = pygame.sprite.Group()
      # Mainmenu
    self.mainmenu_sprites = pygame.sprite.Group()
    self.button_sprites = pygame.sprite.Group()
      # Settings
    self.settings_sprites = pygame.sprite.Group()
    self.settings_slider_sprites = pygame.sprite.Group()
    self.settings_button_sprites = pygame.sprite.Group()
      # Quitmenu
    self.quitmenu_sprites = pygame.sprite.Group()
    self.quitmenu_buttons = pygame.sprite.Group()
      # Sim
    self.sim_sprites = pygame.sprite.Group()
    self.sim_bg_sprite = pygame.sprite.GroupSingle()
    self.collision_sprites = pygame.sprite.Group()
    self.satellite_sprites = pygame.sprite.Group()
    self.orbiting_sprites = pygame.sprite.Group()
    self.trail_sprites = pygame.sprite.Group()
    self.add_mode_arrow = pygame.sprite.GroupSingle()
  
  def create_sprites(self):
    # Create Sprites
    self.create_sim_sprites = CreateSimSprites()
    self.create_sim_sprites.init_sim([self.all_sprites, self.sim_sprites, self.sim_bg_sprite], self.grid_size, [self.all_sprites, self.sim_sprites, self.orbiting_sprites], (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 500)
    self.ui.create_main_menu([self.all_sprites, self.mainmenu_sprites], [self.all_sprites, self.mainmenu_sprites, self.button_sprites])
    self.ui.create_settings_menu([self.all_sprites, self.settings_sprites], [self.all_sprites, self.settings_sprites, self.settings_slider_sprites], [self.all_sprites, self.settings_sprites, self.settings_button_sprites])
    self.ui.create_quitmenu([self.all_sprites, self.quitmenu_sprites], [self.all_sprites, self.quitmenu_sprites, self.quitmenu_buttons])
  
  def mainmenu_events(self, event):
    if self.game_state == 'mainmenu':
      # Keydown events
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.game_state = 'quitmenu'

      # main menu button events
      for button in self.button_sprites:
        if button.hover and event.type == pygame.MOUSEBUTTONDOWN:
          if button.id == 1001:
            self.game_state = 'sim'
            self.sim_music.play_loop()
            self.menu_music.stop()
            pygame.mouse.set_cursor(self.default_cursor)
          if button.id == 1002:
            self.game_state = 'settings'
          if button.id == 1099:
            self.game_state = 'quitmenu'

      if self.game_state == 'mainmenu':
        return False
      else:
        return True

  def quitmenu_events(self, event):
    if self.game_state == 'quitmenu':
      # Keydown events
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.game_state = 'mainmenu'

      # quit menu button events
      for button in self.quitmenu_buttons:
        if button.hover and event.type == pygame.MOUSEBUTTONDOWN:
          if button.id == 9001:
            self.exit_game()
          if button.id == 9002:
            self.game_state = 'mainmenu'

      if self.game_state == 'quitmenu':
        return False
      else:
        return True
  
  def settings_events(self, event):
    if self.game_state == 'settings':
      # watch sliders and button for hover events
      self.ui.detect_hover(self.settings_slider_sprites, self.default_cursor, self.pointer_cursor)
      self.ui.detect_hover(self.settings_button_sprites, self.default_cursor, self.pointer_cursor)
      # keydown events
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.game_state = 'mainmenu'

      for button in self.settings_button_sprites:
        if button.hover and event.type == pygame.MOUSEBUTTONDOWN:
          if button.id == 1198:
            for slider in self.settings_slider_sprites:
              # Game speed
              if slider.id == 1100:
                slider.value = 5
              # Trail length
              if slider.id == 1101:
                self.value = 10
              # Grid size
              if slider.id == 1105:
                self.value = 50
              # Music volume
              if slider.id == 1102:
                self.value = 50
              # Effects volume
              if slider.id == 1103:
                self.value = 25
              # Framerate
              if slider.id == 1104:
                self.value = 60
          if button.id == 1199:
            self.game_state = 'mainmenu'
          
    
      if self.game_state == 'settings':
        return False
      else:
        return True
  
  def sim_events(self, event):
    if self.game_state == 'sim':

      # mouse button events
      if event.type == pygame.MOUSEBUTTONDOWN:
        if self.add_mode:
          self.add_mode = False
          self.create_sim_sprites.Satellite([self.all_sprites, self.sim_sprites, self.satellite_sprites], self.click_pos, self.velocity, self.rand_color, self.orbiting_sprites)
        else:
          self.add_mode = True
          self.click_pos = pygame.mouse.get_pos()
          self.rand_color = (randint(100, 255), randint(100, 255), randint(100, 255))

      # keydown events
      if event.type == pygame.KEYDOWN:
        
        # pause key
        if event.key == pygame.K_p:
          if self.paused:
            self.paused = False
            self.paused_music.stop()
            self.sim_music.play_loop()
          else:
            self.paused = True
            self.sim_music.stop()
            self.paused_music.play_loop()

        # check for escape and go to menu
        if event.key == pygame.K_ESCAPE:
          self.game_state = 'mainmenu'
          self.sim_music.stop()
          self.menu_music.play_loop()
          for sprite in self.satellite_sprites:
            sprite.kill()
            del sprite
          for sprite in self.trail_sprites:
            sprite.kill()
            del sprite

      if self.game_state == 'sim':
        return False
      else:
        return True

  def game_logic(self, dt):
    # Fill screen
    self.screen.fill((0, 0, 0))

    # Game Logic
    self.sim_logic(dt)      
    self.mainmenu_logic(dt)
    self.quitmenu_logic(dt)
    self.settings_logic(dt)
      
  def mainmenu_logic(self, dt):
    # MAIN MENU LOGIC
    if self.game_state == 'mainmenu':
      self.mainmenu_sprites.update(dt)
      self.mainmenu_sprites.draw(self.screen)
      self.ui.detect_hover(self.button_sprites, self.default_cursor, self.pointer_cursor)

  def quitmenu_logic(self, dt):
    # MAIN MENU LOGIC
    if self.game_state == 'quitmenu':
      self.quitmenu_sprites.update(dt)
      self.quitmenu_sprites.draw(self.screen)
      self.ui.detect_hover(self.quitmenu_buttons, self.default_cursor, self.pointer_cursor)

  def settings_logic(self, dt):
    if self.game_state == 'settings':

      # Game Speed
      self.game_speed = self.ui.get_slider_setting(self.settings_slider_sprites, 1100)

      # Trail Length
      self.trail_length = self.ui.get_slider_setting(self.settings_slider_sprites, 1101)

      # Music
      self.menu_music.update_volume(self.ui.get_slider_setting(self.settings_slider_sprites, 1102) / 100)
      self.sim_music.update_volume(self.ui.get_slider_setting(self.settings_slider_sprites, 1102) / 100)
      self.paused_music.update_volume(self.ui.get_slider_setting(self.settings_slider_sprites, 1102) / 100)

      # Sound Effects
      self.crash_sound.update_volume(self.ui.get_slider_setting(self.settings_slider_sprites, 1103) / 100)
      
      # Framerate
      self.framerate = self.ui.get_slider_setting(self.settings_slider_sprites, 1104)

      # Update Grid size
      self.sim_bg_sprite.sprite.grid_size = self.ui.get_slider_setting(self.settings_slider_sprites, 1105)

      # update sprites
      self.settings_sprites.update(dt)
      self.settings_sprites.draw(self.screen)

  def sim_logic(self, dt):
    if self.game_state == 'sim':
      if not self.paused:
        self.physics.collisions(self.satellite_sprites, self.orbiting_sprites, self.crash_sound)
        self.create_sim_sprites.traildots([self.all_sprites, self.sim_sprites, self.trail_sprites], self.satellite_sprites, self.trail_sprites, self.trail_length, dt)
        self.sim_sprites.update(dt)
      self.sim_sprites.draw(self.screen)
      
      if self.add_mode:
        self.velocity = self.ui.add_mode(self.screen, self.click_pos, self.default_font, self.rand_color)

  def find_dt(self, last_time):
    dt = (pygame.time.get_ticks() - last_time) / (100 / self.game_speed)
    last_time = pygame.time.get_ticks()
    return dt, last_time

  def save_settings(self):
    # save settings
    file_path = 'settings.py'
    window_width = self.window_width
    window_height = self.window_height
    framerate = self.ui.get_slider_setting(self.settings_slider_sprites, 1104)
    init_game_state = str(INITIAL_GAME_STATE)
    game_speed = self.ui.get_slider_setting(self.settings_slider_sprites, 1100)
    trail_length = self.ui.get_slider_setting(self.settings_slider_sprites, 1101)
    grid_size = self.ui.get_slider_setting(self.settings_slider_sprites, 1105)
    music_volume = self.ui.get_slider_setting(self.settings_slider_sprites, 1102)
    effects_volume = self.ui.get_slider_setting(self.settings_slider_sprites, 1103)

    with open(file_path, 'w') as f:
      f.write(f'WINDOW_WIDTH = {window_width}\n')
      f.write(f'WINDOW_HEIGHT = {window_height}\n')
      f.write(f'FRAMERATE = {framerate}\n')
      f.write(f'INITIAL_GAME_STATE = "{init_game_state}"\n')
      f.write(f'GAME_SPEED = {game_speed}\n')
      f.write(f'TRAIL_LENGTH = {trail_length}\n')
      f.write(f'GRIDSIZE = {grid_size}\n')
      f.write(f'MUSIC_VOLUME = {music_volume}\n')
      f.write(f'EFFECTS_VOLUME = {effects_volume}\n')
  
  def exit_game(self):
    self.save_settings()

    pygame.quit()
    sys.exit()
    
  def run(self):
    last_time = pygame.time.get_ticks()

    # PYGAME WHILE LOOP
    while True:

      # delta time
      dt, last_time = self.find_dt(last_time)

      # event loop
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.exit_game()

        # Main menu events 
        game_state_changed = self.mainmenu_events(event)
        if game_state_changed:
          continue

        # Quit menu events
        game_state_changed = self.quitmenu_events(event)
        if game_state_changed:
          continue
        
        # settings events
        game_state_changed = self.settings_events(event)
        if game_state_changed:
          continue

        # simulator events
        game_state_changed = self.sim_events(event)
        if game_state_changed:
          continue

      # Game logic
      self.game_logic(dt)
  
      # Update screen
      pygame.display.update()
      self.clock.tick(self.framerate)

if __name__ == '__main__':
  game = Game()
  game.run()