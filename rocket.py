import pygame
from pygame.math import Vector2

class Rocket(object):
    def __init__(self, game):
        self.game = game
        self.speed = 1.0
        self.gravity = 0.5

        size = self.game.screen1.get_size()

        self.pos = Vector2(size[0] / 2, size[1] / 2)  # Inicjalizacja pozycji rakiety
        self.vel = Vector2(0, 0)  # Inicjalizacja prędkości rakiety
        self.acc = Vector2(0, 0)  # Inicjalizacja przyspieszenia rakiety

        self.obj_width = 100  # Szerokość rakiety
        self.obj_height = 100  # Wysokość rakiety

    def add_force(self, force):
        self.acc += force

    def tick(self):
        # klawka input
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_s]:
            self.add_force(Vector2(0, self.speed))
        if pressed[pygame.K_w]:
            self.add_force(Vector2(0, -self.speed))
        if pressed[pygame.K_a]:
            self.add_force(Vector2(-self.speed, 0))
        if pressed[pygame.K_d]:
            self.add_force(Vector2(self.speed, 0))

        # Sprawdzenie czy obiekt nie wychodzi poza ekran widoczny
        WIDTH, HEIGHT = self.game.screen1.get_size()
        self.pos.x = max(0, min(self.pos.x, WIDTH - self.obj_width))  # Ograniczenie ruchu w poziomie
        self.pos.y = max(0, min(self.pos.y, HEIGHT - self.obj_height))  # Ograniczenie ruchu w pionie

        # Sprawdzenie kolizji z przeszkodą
        #for wall in self.game.walls:
           # if self.pos.colliderect(wall):
           #     self.vel *= -0.5  # Odwrócenie kierunku ruchu

        # fiz
        self.vel *= 0.8  # Zmniejszenie prędkości (opór powietrza)
        self.vel -= Vector2(0, -self.gravity)  # Dodanie siły grawitacji
        self.vel += self.acc  # Dodanie przyspieszenia
        self.pos += self.vel  # Zaktualizowanie pozycji
        self.acc *= 0  # Resetowanie przyspieszenia

    def draw(self):
        # podstawowy trujkont
        points = [Vector2(0, -10), Vector2(5, 5), Vector2(-5, 5)]
        # rotate obracanie
        angle = self.vel.angle_to(Vector2(0, 1))
        points = [p.rotate(angle) for p in points]
        # fix Y
        points = [Vector2(p.x, p.y * -1) for p in points]

        # Add current pos
        points = [self.pos + p * 4 for p in points]
        # drow triangle
        pygame.draw.polygon(self.game.screen1, (200, 100, 0), points)


class Game(object):
    def __init__(self):
        # Inicjalizacja
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen1 = pygame.display.set_mode((self.WIDTH, self.HEIGHT))  # Ustawienie rozmiaru okna

        # Inicjalizacja rakiety
        self.rocket = Rocket(self)

        # Inicjalizacja ścian
        self.wall_x = 400
        self.wall_y = 300
        self.wall_width = 200
        self.wall_height = 50
        self.walls = pygame.Rect(self.wall_x, self.wall_y, self.wall_width, self.wall_height)

        # Start gry
        self.run_game()

    def run_game(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen1.fill((0, 0, 0))  # Wypełnienie ekranu kolorem czarnym
            self.update()
            pygame.display.flip()  # Odświeżenie ekranu
            clock.tick(60)  # Ustawienie limitu klatek na sekundę

    def update(self):
        self.rocket.tick()  # Aktualizacja stanu rakiety
        pygame.draw.rect(self.screen1, (255, 255, 255), self.walls)  # Rysowanie ściany
        self.rocket.draw()  # Rysowanie rakiety



if __name__ == "__main__":
    Game()  # Rozpoczęcie gry
