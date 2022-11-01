import pygame
from settings import *

class UI():
  def __init__(self):
    pass

  def draw_vector_arrow(self, surface, color, start_pos):
    line_width = 4
    pygame.draw.line(surface, color, (0, 0), pygame.mouse.get_pos(), line_width)
