import sys
from pathlib import Path
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

assets_path = Path(__file__).parent / 'assets'

pygame.init()
pygame.font.init()
pygame.mixer.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Load assets
        self.bg = pygame.image.load(assets_path / 'bg.png')
        self.font_large = pygame.font.Font(assets_path / 'font.ttf', 150)
        self.font_small = pygame.font.Font(assets_path / 'font.ttf', 50)
        self.split_files = sorted(assets_path.rglob('bang?.wav'))
        self.split_sounds = [pygame.mixer.Sound(f) for f in self.split_files]
        self.shot_sound = pygame.mixer.Sound(assets_path / 'fire.wav')

        # Set groups
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()

        # Assign containers
        Player.containers = (self.updatable, self.drawable)
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, self.shot_sound)

        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable)
        self.asteroidfield = AsteroidField(self.split_sounds)
        
        Shot.containers = (self.shots, self.updatable, self.drawable)

    def title_screen(self):
        self.screen.fill('black')
        self.screen.blit(self.bg, (0,0))

        title_text = self.font_large.render('Asteroids', True, 'white')
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(title_text, title_rect)

        instruct_text = self.font_small.render('Press space to begin', True, 'white')
        instruct_rect = instruct_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 250))
        self.screen.blit(instruct_text, instruct_rect)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return 'play'
                
    def play(self):
        dt = 0
        
        while True:
            self.screen.fill('black')
            self.screen.blit(self.bg, (0,0))

            self.updatable.update(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            for asteroid in self.asteroids:
                if asteroid.check_collision(self.player):
                    return 'game_over'
                for shot in self.shots:
                    if shot.check_collision(asteroid):
                        shot.kill()
                        asteroid.split()

            for obj in self.drawable:
                obj.draw(self.screen)

            pygame.display.flip()
            dt = self.clock.tick(60) / 1000



    def game_over(self):
        title_text = self.font_large.render('Game over!', True, 'white')
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(title_text, title_rect)
        
        instruct_text = self.font_small.render('Space to respawn', True, 'white')
        instruct_text_2 = self.font_small.render('Escape to quit', True, 'white')
        instruct_rect = instruct_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 250))
        instruct_rect_2 = instruct_text_2.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 200))
        self.screen.blit(instruct_text, instruct_rect)
        self.screen.blit(instruct_text_2, instruct_rect_2)
        
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.reset_game()
                    return 'play'
    
    def reset_game(self):
        self.updatable.empty()
        self.drawable.empty()
        self.asteroids.empty()
        self.shots.empty()

        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, self.shot_sound)
        self.asteroidfield = AsteroidField(self.split_sounds)
        # self.asteroids.reset()

        
if __name__ == "__main__":
    game = Game()

    state = game.title_screen()
    while True:
        if state == 'play':
            state = game.play()
        elif state == 'game_over':
            state = game.game_over()