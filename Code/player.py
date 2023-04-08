import pygame
from support import ImportFolder
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__();
        self.importCharacterAssets();
        self.frameIndex = 0;
        self.animationSpeed = 0.15;
        self.image = self.animations["idle"][self.frameIndex];
        self.rect = self.image.get_rect(topleft = pos);

        # movement
        self.direction = pygame.math.Vector2((0,0));
        self.baseSpeed = 10;
        self.speed = self.baseSpeed;
        self.gravity = 0.8;
        self.jumpForce = -16;
    
        self.state = "idle";
    
    def importCharacterAssets(self):
        PATH = "./Graphics/Character/";
        self.animations = {
                            "idle": [],
                            "run": [],
                            "jump": [],
                            "fall": []
                        }
        for animation in self.animations.keys():
            fullPath = PATH + animation;
            self.animations[animation] = ImportFolder(fullPath); 
    
    def Animate(self):
        animation = self.animations[self.state];
    
        # Loop on frame index
        self.frameIndex += self.animationSpeed;

        if(self.frameIndex > len(animation)):
            self.frameIndex = 0;

        self.image = animation[int(self.frameIndex)];
    
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
    
    def CheckState(self):
        dir = self.direction;

        if(math.fabs(dir.y) > 0):
            if(dir.y < 0):
                self.state = "jump";
            elif(dir.y > 1):
                self.state = "fall";
        else:
            if(math.fabs(dir.x) > 0):
                self.state = "run";
            else: 
                self.state = "idle"

    def ApplyGravity(self):
        self.direction.y += self.gravity;
        self.rect.y += self.direction.y;
    
    def Jump(self):
        self.direction.y = self.jumpForce;

    def update(self):
        self.GetInput();
        self.CheckState();
        self.Animate();
        # self.rect.x += self.direction.x * self.speed;
        # self.ApplyGravity();