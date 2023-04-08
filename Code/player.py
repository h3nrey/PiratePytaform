import pygame
from support import ImportFolder
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, screen, createJumpParticles):
        super().__init__();
        self.importCharacterAssets();
        self.frameIndex = 0;
        self.animationSpeed = 0.15;
        self.image = self.animations["idle"][self.frameIndex];
        self.rect = self.image.get_rect(topleft = pos);

        # particles
        self.importDustRunParticles();
        self.dustFrameIndex = 0;
        self.dustAnimationSpeed = 0.15;
        self.displaySurf = screen;
        self.createJumpParticles = createJumpParticles;
        
        # movement
        self.direction = pygame.math.Vector2((0,0));
        self.baseSpeed = 10;
        self.speed = self.baseSpeed;
        self.gravity = 0.8;
        self.jumpForce = -16;

        # States
        self.state = "idle";
        self.isFacingRight = True;
        self.onGround = True;
        self.onCeiling = False;
        self.onRight = False;
        self.onLeft = False;
    
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
    
    def importDustRunParticles(self):
        self.dustRunParticles = ImportFolder("./Graphics/Character/DustParticles/run")
    
    # Animations
    def Animate(self):
        animation = self.animations[self.state];
    
        # Loop on frame index
        self.frameIndex += self.animationSpeed;

        if(self.frameIndex > len(animation)):
            self.frameIndex = 0;

        image = animation[int(self.frameIndex)];
        if(self.isFacingRight):
            self.image = image;
        else:
            flippedImage = pygame.transform.flip(image, True, False);
            self.image = flippedImage;
    
        # Set rect
        if(self.onGround and self.onRight):
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright);
        elif(self.onGround and self.onLeft):
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft);
        elif(self.onGround):
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom);
        
        elif(self.onCeiling and self.onRight):
            self.rect = self.image.get_rect(topright = self.rect.topright);
        elif(self.onCeiling and self.onLeft):
            self.rect = self.image.get_rect(topleft = self.rect.topleft);
        elif(self.onCeiling):
            self.rect = self.image.get_rect(midtop = self.rect.midtop);
    
    def RunDustAnimations(self):
        if(self.state == "run" and self.onGround):
            self.dustFrameIndex += self.dustAnimationSpeed;
            if(self.dustFrameIndex > len(self.dustRunParticles)): 
                self.dustFrameIndex = 0;

            dustParticles = self.dustRunParticles[int(self.dustFrameIndex)];
    
            if(self.isFacingRight):
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10);
                self.displaySurf.blit(dustParticles, pos);
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6,10);
                flippedDust = pygame.transform.flip(dustParticles, True, False);
                self.displaySurf.blit(flippedDust, pos);
    
    def GetInput(self):
        keys = pygame.key.get_pressed();
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1;
            self.isFacingRight = True;
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1;
            self.isFacingRight = False;
        else:
            self.direction.x = 0;
    
        if keys[pygame.K_SPACE]:
            self.Jump();
            self.createJumpParticles(self.rect.midbottom);
    
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
        if(self.onGround):
            self.direction.y = self.jumpForce;

    def update(self):
        self.GetInput();
        self.CheckState();
        self.Animate();
        self.RunDustAnimations();
        # self.rect.x += self.direction.x * self.speed;
        # self.ApplyGravity();