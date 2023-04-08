import pygame;
from support import ImportFolder;

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__();
        self.frameIndex = 0;
        self.animationSpeed = 0.5;

        if(type == "jump"):
            self.frames = ImportFolder("./Graphics/Character/DustParticles/jump")
        if(type == "land"):
            self.frames = ImportFolder("./Graphics/Character/DustParticles/land")

        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_rect(center = pos);

    def Animate(self):
        self.frameIndex += self.animationSpeed;
        
        if(self.frameIndex > len(self.frames) - 1):
            self.kill();
        else:
            self.image = self.frames[int(self.frameIndex)];
    def update(self, xShift):
        self.Animate();
        self.rect.x += xShift
