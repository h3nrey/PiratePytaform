import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__();
        self.image = pygame.Surface((32,64));
        self.image.fill("green");
        self.rect = self.image.get_rect(topleft = pos);

        # movement
        self.direction = pygame.math.Vector2((0,0));
        self.baseSpeed = 10;
        self.speed = self.baseSpeed;
        self.gravity = 0.8;
        self.jumpForce = -16;
    
    def GetInput(self):
        keys = pygame.key.get_pressed();
        print("input");
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1;
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1;
        else:
            self.direction.x = 0;
    
        if keys[pygame.K_SPACE]:
            self.Jump();
    
    def ApplyGravity(self):
        self.direction.y += self.gravity;
        self.rect.y += self.direction.y;
    
    def Jump(self):
        self.direction.y = self.jumpForce;

    def update(self):
        self.GetInput();
        # self.rect.x += self.direction.x * self.speed;
        # self.ApplyGravity();