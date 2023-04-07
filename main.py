import pygame , sys;

pygame.init();
screenW = 1200;
screenH = 700;
screen = pygame.display.set_mode((screenW, screenH));

clock = pygame.time.Clock();
FPS = 60;

while True:
    events = pygame.event.get();
    for event in events:
        if(event.type == pygame.QUIT):
            pygame.quit();
            sys.exit();

    screen.fill("black");

    pygame.display.update();
    clock.tick(FPS);