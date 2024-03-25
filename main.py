import pygame
import sys
from rocket import Rocket
from objekty import objekty

class Game(object):
    obj_height = 1280
    obj_width = 720

    def __init__(self):
        # Config
        self.create_object_timer = 0
        self.clock = pygame.time.Clock()
        self.max_tps = 200.0
        do = True

        # Inicjalizacja
        pygame.init()
        self.screen1 = pygame.display.set_mode((Game.obj_height, Game.obj_width))
        pygame.display.set_caption("Gra unikanie")
        self.clock_tps = pygame.time.Clock()
        self.tps_czas = 0.0

        self.image = pygame.image.load("xd.jpg")  # Dodaj atrybut image

        self.objekty = objekty(self)
        self.gracz = Rocket(self)

        while True:
            # Zamknięcie okna
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            # Okresy czasowe Tick
            self.tps_czas += self.clock_tps.tick() / 1000.0
            while self.tps_czas > 1 / self.max_tps:
                self.tick()
                self.tps_czas -= 1 / self.max_tps

            # Render
            self.screen1.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()

    def background(self):
        size = pygame.transform.scale(self.image, (Game.obj_height, Game.obj_width))
        self.screen1.blit(size, (0, 0))

    def tick(self):
        self.gracz.tick()
        self.objekty.tick()

        # Sprawdzamy, czy czas na utworzenie nowego obiektu
        self.create_object_timer += self.clock_tps.get_time() / 1000.0
        if self.create_object_timer >= 2:  # Jeśli minęło co najmniej 2 sekundy
            self.create()  # Tworzymy nowy obiekt
            self.create_object_timer = 0  # Resetujemy licznik czasu

    def draw(self):
        # tło
        self.background()
        # gracz
        self.gracz.draw()
        # obiekty
        self.objekty.draw()

    def create(self):
        self.objekty.draw()  # Rysujemy nowy obiekt

if __name__ == "__main__":
    game = Game()