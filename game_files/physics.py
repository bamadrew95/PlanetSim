import pygame
import math

pygame_vector = object

class Physics:
  def __init__(self):
    self.piovertwo = math.pi / 2
    self.pi = math.pi
    self.threepiovertwo = (3 * math.pi) / 2

  def collisions(self, destroy_group, do_not_destroy_group, crash_sound):
    for sprite in destroy_group:
      if pygame.sprite.spritecollide(sprite, do_not_destroy_group, False):
        crash_sound.play()
        sprite.kill()
        del sprite

  def gravitational_force(self, obj_mass: int, obj_pos: pygame_vector, sprite_pos: pygame_vector):
    rel_pos = sprite_pos - obj_pos
    rel_pos.y = -rel_pos.y

    distance_tuple = (abs(rel_pos.x), abs(rel_pos.y))

    distance = math.sqrt(math.pow(rel_pos.x, 2) + math.pow(rel_pos.y, 2))

    # calc gravitational strength
    if distance and distance < 1000:
      gravity_scalar = obj_mass / math.pow(distance, 2)
    else:
      gravity_scalar = 0

    theta = self.find_angle((rel_pos.x, rel_pos.y), distance_tuple)

    # calc change in speed
    grav_force_x = math.cos(theta) * gravity_scalar
    grav_force_y = math.sin(theta) * gravity_scalar

    gravitational_force = pygame.math.Vector2((grav_force_x, grav_force_y))
    return gravitational_force

  def find_angle(self, rel_pos: tuple, distance_tuple: tuple):
    # find quadrant
      if rel_pos[0] >= 0 and rel_pos[1] < 0:
        quad = 1
      elif rel_pos[0] < 0 and rel_pos[1] < 0:
        quad = 2
      elif rel_pos[0] < 0 and rel_pos[1] >= 0:
        quad = 3
      else:
        quad = 4

      # calc theta
      if quad == 1:
        if distance_tuple[0]:
          theta = math.atan(distance_tuple[1] / distance_tuple[0])
        else:
          theta = self.piovertwo

      if quad == 2:
        if distance_tuple[1]:
          theta = (math.atan(distance_tuple[0] / distance_tuple[1])) + (self.piovertwo)
        else:
          theta = self.pi
      
      if quad == 3:
        if distance_tuple[0]:
          theta = (math.atan(distance_tuple[1] / distance_tuple[0])) + (self.pi)
        else:
          theta = self.threepiovertwo / 2

      if quad == 4:
        if distance_tuple[1]:
          theta = (math.atan(distance_tuple[0] / distance_tuple[1])) + (self.threepiovertwo)
        else:
          theta = 0
      
      return theta
