import pygame
from pygame.math import Vector2
import random  # Import modułu random

class objekty(object):
    def __init__(self, game):
        self.game = game
        self.speed = 1.0
        self.gravity = 0.2  # Zmniejszamy wartość grawitacji

        size = self.game.screen1.get_size()

        # Losowe położenie poziome, stała pozycja wzdłuż osi Y
        self.pos = Vector2(random.randint(0, size[0]), 0)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

        self.obj_width = 100
        self.obj_height = 100

    def tick(self):
        self.vel *= 0.8
        self.vel += Vector2(0, self.gravity)  # Dodajemy siłę grawitacji
        self.pos += self.vel
        # Nie zerujemy przyspieszenia, aby uwzględnić siłę grawitacji w następnych iteracjach

    def draw(self):
        # Definiujemy wierzchołki kwadratu
        half_width = 25  # Połowa szerokości kwadratu
        half_height = 25  # Połowa wysokości kwadratu
        points = [
            Vector2(-half_width, -half_height),
            Vector2(half_width, -half_height),
            Vector2(half_width, half_height),
            Vector2(-half_width, half_height)
        ]
        # Obracamy kwadrat zgodnie z kierunkiem prędkości
        angle = self.vel.angle_to(Vector2(0, 1))
        points = [p.rotate(angle) for p in points]
        # Przesuwamy kwadrat na jego aktualną pozycję
        points = [self.pos + p for p in points]
        # Rysujemy kwadrat
        pygame.draw.polygon(self.game.screen1, (250, 10, 10), points)









class Game(object):
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen1 = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.rocket = objekty(self)

        self.wall_x = 400
        self.wall_y = 300
        self.wall_width = 200
        self.wall_height = 50
        self.walls = pygame.Rect(self.wall_x, self.wall_y, self.wall_width, self.wall_height)

        self.run_game()

    def run_game(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen1.fill((0, 0, 0))
            self.update()
            pygame.display.flip()
            clock.tick(60)

    def update(self):
        self.rocket.tick()
        pygame.draw.rect(self.screen1, (255, 255, 255), self.walls)
        self.rocket.draw()

if __name__ == "__main__":
    Game()
