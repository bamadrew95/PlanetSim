import pygame
import math

pygame_vector = object

class Physics:
  def __init__(self):
    self.piovertwo = math.pi / 2
    self.pi = math.pi
    self.threepiovertwo = (3 * math.pi) / 2

  def gravitational_force(self, obj_mass: int, obj_pos: pygame_vector, sprite_pos: pygame_vector):
    rel_pos = sprite_pos - obj_pos
    rel_pos.y = -rel_pos.y

    distance_vect = pygame.math.Vector2((abs(rel_pos.x), abs(rel_pos.y)))

    distance = math.sqrt(math.pow(rel_pos.x, 2) + math.pow(rel_pos.y, 2))

    # calc gravitational strength
    if distance and distance < 1000:
      gravity_scalar = obj_mass / math.pow(distance, 2)
    else:
      gravity_scalar = 0

    # find quadrant
    if rel_pos.x >= 0 and rel_pos.y < 0:
      quad = 1
    elif rel_pos.x < 0 and rel_pos.y < 0:
      quad = 2
    elif rel_pos.x < 0 and rel_pos.y >= 0:
      quad = 3
    else:
      quad = 4

    # calc theta
    if quad == 1:
      if distance_vect.x:
        theta = math.atan(distance_vect.y / distance_vect.x)
      else:
        theta = self.piovertwo

    if quad == 2:
      if distance_vect.y:
        theta = (math.atan(distance_vect.x / distance_vect.y)) + (self.piovertwo)
      else:
        theta = self.pi
    
    if quad == 3:
      if distance_vect.x:
        theta = (math.atan(distance_vect.y / distance_vect.x)) + (self.pi)
      else:
        theta = self.threepiovertwo / 2

    if quad == 4:
      if distance_vect.y:
        theta = (math.atan(distance_vect.x / distance_vect.y)) + (self.threepiovertwo)
      else:
        theta = 0

    # calc change in speed
    grav_force_x = math.cos(theta) * gravity_scalar
    grav_force_y = math.sin(theta) * gravity_scalar

    gravitational_force = pygame.math.Vector2((grav_force_x, grav_force_y))
    return gravitational_force