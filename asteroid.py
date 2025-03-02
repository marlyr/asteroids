import random
import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, split_sounds):
        super().__init__(x, y, radius)
        self.split_sounds = split_sounds
    
    def draw(self, screen):
        pygame.draw.circle(screen, 'white', self.position, self.radius)
    
    def update(self, dt):
        self.position += self.velocity * dt

    def get_asteroid_size(self):
        if self.radius <= ASTEROID_MIN_RADIUS:
            return 0
        elif self.radius < ASTEROID_MAX_RADIUS:
            return 1
        else:
            return 2

    def split(self):
        self.kill()

        size = self.get_asteroid_size()
        self.split_sounds[size].play()

        if size == 0:
            return
        
        random_angle = random.uniform(20, 50)
        v1 = self.velocity.rotate(random_angle)
        v2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        ast1 = Asteroid(self.position[0], self.position[1], new_radius, self.split_sounds)
        ast2 = Asteroid(self.position[0], self.position[1], new_radius, self.split_sounds)

        ast1.velocity = v1 * 1.2
        ast2.velocity = v2 * 1.2