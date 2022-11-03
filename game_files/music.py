import pygame
from settings import *

class Music():
  def __init__(self, file_name, volume):
    f = 'assets/audio/' + file_name
    self.volume = volume / 100

    self.music = pygame.mixer.Sound(f)
    self.music.set_volume(self.volume)
  
  def update_volume(self, volume):
    self.volume = volume
    self.music.set_volume(self.volume)
  
  def play(self):
    self.music.play(loops = -1)

  def stop(self):
    self.music.stop()