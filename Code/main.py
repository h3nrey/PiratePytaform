import pygame , sys;
from settings import *
from level import Level

# Pygame setup
pygame.init();
screenW = 1200;
screenH = 700;
screen = pygame.display.set_mode((screenW, screenH));

clock = pygame.time.Clock();
FPS = 60;

level = Level(levelMap, screen); 

while True:
    events = pygame.event.get();
    for event in events:
        if(event.type == pygame.QUIT):
            pygame.quit();
            sys.exit();

    screen.fill("black");
    level.run ();

    pygame.display.update();
    clock.tick(FPS);