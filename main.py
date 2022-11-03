import pygame, sys, time
from settings import *
from game_files.sprites.sim import CreateSprites
from game_files.sprites.ui import UI
from game_files.physics import Physics
from game_files.audio import Sound
from random import randint

class Game():
  def __init__(self):
    # import settings
    self.window_width = WINDOW_WIDTH
    self.window_height = WINDOW_HEIGHT
    self.framerate = FRAMERATE
    self.game_state = INITIAL_GAME_STATE
    self.game_speed = GAME_SPEED
    self.trail_length = TRAIL_LENGTH

    # Initialization of pygame window
    pygame.init()
    self.screen = pygame.display.set_mode((self.window_width, self.window_height))
    pygame.display.set_caption('Planet Simulator')
    self.clock = pygame.time.Clock()

    # Cursors
    self.default_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
    self.pointer_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
    pygame.mouse.set_cursor(self.default_cursor)

    # Fonts
    self.default_font = pygame.font.Font('assets/fonts/Pixeltype.ttf', 24)

    # initial states
    self.paused = False
    self.click_pos = (0, 0)
    self.add_mode = False
    self.velocity_selector = (0, 0)

    # run game_files
    self.ui = UI()
    self.physics = Physics()

    # audio
      # music
    self.menu_music = Sound('Acadia.mp3', MUSIC_VOLUME)
    self.sim_music = Sound('DreamyFlashback.mp3', MUSIC_VOLUME)
    self.paused_music = Sound('FrozenStar.mp3', MUSIC_VOLUME)
    self.menu_music.play_loop()
      # sound effects
    self.crash_sound = Sound('impact.mp3', EFFECTS_VOLUME)

    # Sprite groups
    self.all_sprites = pygame.sprite.Group()
    self.mainmenu_sprites = pygame.sprite.Group()
    self.button_sprites = pygame.sprite.Group()
    self.settingsmenu_sprites = pygame.sprite.Group()
    self.slider_sprites = pygame.sprite.Group()
    self.dialogue_sprites = pygame.sprite.Group()
    self.dialogue_button_sprites = pygame.sprite.Group()
    self.sim_sprites = pygame.sprite.Group()
    self.collision_sprites = pygame.sprite.Group()
    self.satellite_sprites = pygame.sprite.Group()
    self.orbiting_sprites = pygame.sprite.Group()
    self.trail_sprites = pygame.sprite.Group()
    self.add_mode_arrow = pygame.sprite.GroupSingle()

    self.create_sprites = CreateSprites()
    self.create_sprites.init_sim([self.all_sprites, self.sim_sprites], [self.all_sprites, self.sim_sprites, self.orbiting_sprites], (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 500)
    self.ui.create_main_menu([self.all_sprites, self.mainmenu_sprites], [self.all_sprites, self.mainmenu_sprites, self.button_sprites])
    self.ui.create_settings_menu([self.all_sprites, self.settingsmenu_sprites], [self.all_sprites, self.settingsmenu_sprites, self.slider_sprites])

  def toggle_quit_dialogue(self):
    if hasattr(self, 'quit_dialogue'):
      self.dialogue_sprites.empty()
      del self.quit_dialogue
    else:
      self.quit_dialogue = self.ui.DialogueBox([self.all_sprites, self.dialogue_sprites], [self.all_sprites, self.dialogue_sprites, self.dialogue_button_sprites], 'Are you sure you want to quit?', 'Yes', 'No', self.exit_game)

  def exit_game(self):
    # save settings
    file_path = 'settings.py'
    window_width = WINDOW_WIDTH
    window_height = WINDOW_HEIGHT
    framerate = self.ui.get_slider_setting(self.slider_sprites, 1104)
    init_game_state = str(INITIAL_GAME_STATE)
    game_speed = self.ui.get_slider_setting(self.slider_sprites, 1100)
    trail_length = self.ui.get_slider_setting(self.slider_sprites, 1101)
    unitsize = UNITSIZE
    music_volume = self.ui.get_slider_setting(self.slider_sprites, 1102)
    effects_volume = self.ui.get_slider_setting(self.slider_sprites, 1103)
    
    with open(file_path, 'w') as f:
        f.write(f'WINDOW_WIDTH = {window_width}\n')
        f.write(f'WINDOW_HEIGHT = {window_height}\n')
        f.write(f'FRAMERATE = {framerate}\n')
        f.write(f'INITIAL_GAME_STATE = "{init_game_state}"\n')
        f.write(f'GAME_SPEED = {game_speed}\n')
        f.write(f'TRAIL_LENGTH = {trail_length}\n')
        f.write(f'UNITSIZE = {unitsize}\n')
        f.write(f'MUSIC_VOLUME = {music_volume}\n')
        f.write(f'EFFECTS_VOLUME = {effects_volume}\n')

    # exit game
    pygame.quit()
    sys.exit()

  def run(self):
    last_time = pygame.time.get_ticks()

    while True:

      # delta time
      dt = (pygame.time.get_ticks() - last_time) / (100 / self.game_speed)
      last_time = pygame.time.get_ticks()

      # event loop
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.exit_game()

        # MAIN MENU EVENTS
        if self.game_state == 'mainmenu':

          # Keydown events
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
              self.toggle_quit_dialogue()

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
          
          # Dialogue button events
          for button in self.dialogue_button_sprites:
            if button.hover and event.type == pygame.MOUSEBUTTONDOWN and hasattr(self, 'quit_dialogue'):
              if button.id == 9001:
                self.quit_dialogue.run()
              if button.id == 9002:
                self.dialogue_sprites.empty()
                del self.quit_dialogue

          if self.game_state != 'mainmenu':
            continue

        # SETTINGS MENU EVENTS
        if self.game_state == 'settings':

          # keydown events
          if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
              self.game_state = 'mainmenu'

          if self.game_state != 'settings':
            continue

        # SIMULATOR EVENTS
        if self.game_state == 'sim':

          # mouse button events
          if event.type == pygame.MOUSEBUTTONDOWN:
            if self.add_mode:
              self.add_mode = False
              self.ui.add_satellite([self.all_sprites, self.sim_sprites, self.satellite_sprites], self.click_pos, self.velocity, self.rand_color, self.orbiting_sprites)
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

          if self.game_state != 'sim':
            continue      

      # End event loop

      self.screen.fill((0, 0, 0))
      
      # SIMULATOR GAME LOGIC
      if self.game_state == 'sim':
        if not self.paused:
          self.physics.collisions(self.satellite_sprites, self.orbiting_sprites, self.crash_sound)
          self.create_sprites.traildots([self.all_sprites, self.sim_sprites, self.trail_sprites], self.satellite_sprites, self.trail_sprites, self.trail_length, dt)
          self.sim_sprites.update(dt)
        self.sim_sprites.draw(self.screen)
        
        if self.add_mode:
          self.velocity = self.ui.add_mode(self.screen, self.click_pos, self.default_font, self.rand_color)

      # MAIN MENU LOGIC
      if self.game_state == 'mainmenu':
        self.mainmenu_sprites.update(dt)
        self.mainmenu_sprites.draw(self.screen)

        # Quit dialogue
        if not hasattr(self, 'quit_dialogue'):
          self.ui.detect_hover(self.button_sprites, self.default_cursor, self.pointer_cursor)
        else:
          self.dialogue_sprites.update(dt)
          self.dialogue_sprites.draw(self.screen)
          self.ui.detect_hover(self.dialogue_button_sprites, self.default_cursor, self.pointer_cursor)

      # SETTINGS MENU LOGIC
      if self.game_state == 'settings':

        # Game Speed
        self.game_speed = self.ui.get_slider_setting(self.slider_sprites, 1100)

        # Trail Length
        self.trail_length = self.ui.get_slider_setting(self.slider_sprites, 1101)

        # Music
        self.menu_music.update_volume(self.ui.get_slider_setting(self.slider_sprites, 1102) / 100)
        self.sim_music.update_volume(self.ui.get_slider_setting(self.slider_sprites, 1102) / 100)
        self.paused_music.update_volume(self.ui.get_slider_setting(self.slider_sprites, 1102) / 100)

        # Sound Effects
        self.crash_sound.update_volume(self.ui.get_slider_setting(self.slider_sprites, 1103) / 100)
        
        # Framerate
        self.framerate = self.ui.get_slider_setting(self.slider_sprites, 1104)

        # watch sliders for hover events
        self.ui.detect_hover(self.slider_sprites, self.default_cursor, self.pointer_cursor)

        # update sprites
        self.settingsmenu_sprites.update(dt)
        self.settingsmenu_sprites.draw(self.screen)

      pygame.display.update()
      self.clock.tick(self.framerate)

if __name__ == '__main__':
  game = Game()
  game.run()