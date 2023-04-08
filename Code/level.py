import pygame, math
from tiles import Tile;
from settings import tileSize, screenW, camBorder;
from player import Player;
from particles import ParticleEffect;

class Level:
    def __init__(self, levelData, surface):
        self.displaySurf = surface;
        self.setupLevel(levelData);
        self.worldShift = 0;
        self.lastCollisionXPos = 0;
    
        # Dust
        self.dustSprite = pygame.sprite.GroupSingle();
        self.playerOnGround = False;
    
    def CreateJumpParticles(self, pos):
        if(self.player.sprite.isFacingRight):
            pos -= pygame.math.Vector2(10,5);
        else:
            pos += pygame.math.Vector2(10, -5);
        jumpParticleSprite = ParticleEffect(pos,"jump");
        self.dustSprite.add(jumpParticleSprite);

    def CreateLandingDust(self):
        if(not self.playerOnGround and self.player.sprite.onGround and not self.dustSprite.sprites()):
            if(self.player.sprite.isFacingRight):
                offset  = pygame.math.Vector2(10,15);
            else:
                offset  = pygame.math.Vector2(-10,15);
            fallDustParticle = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land");
            self.dustSprite.add(fallDustParticle);
    def setupLevel(self, layout):
        self.tiles = pygame.sprite.Group();
        self.player = pygame.sprite.GroupSingle();

        for rowIndex, row in enumerate(layout):
            for cellIndex, cell in enumerate(row):
                x, y = cellIndex * tileSize, rowIndex * tileSize;
                if(cell == "X"): 
                    tile = Tile((x,y), tileSize)
                    self.tiles.add(tile);
                if(cell == "P"):
                    playerSpr = Player((x,y), self.displaySurf, self.CreateJumpParticles);
                    self.player.add(playerSpr);
    
    def ScrollX(self):
        player = self.player.sprite;
        playerX = player.rect.centerx;
        playerDir = player.direction.x;
        
        if(math.fabs(playerDir) > 0):
            if(playerX < camBorder):
                self.worldShift = player.baseSpeed;
                player.speed = 0;
            if(playerX > screenW - camBorder):
                self.worldShift = -player.baseSpeed;
                player.speed = 0;
        else:
            self.worldShift = 0;
            player.speed = player.baseSpeed;

    def GetPlayerOnGround(self):
        if(self.player.sprite.onGround):
            self.playerOnGround = True;
        else:
            self.playerOnGround = False;
    
    def HorizontalMovementCollision(self):
        player = self.player.sprite;
        player.rect.x += player.direction.x * player.speed;
    
        for sprite in self.tiles.sprites():
            if(sprite.rect.colliderect(player.rect)):
                if(player.direction.x < 0):
                    player.rect.left = sprite.rect.right;
                    player.onLeft = True;
                    self.lastCollisionXPos = player.rect.left;
                elif(player.direction.x > 0):
                    player.rect.right = sprite.rect.left;
                    player.onRight = True;
                    self.lastCollisionXpos = player.rect.right;
        
        if(player.onLeft and (player.rect.left < self.lastCollisionXPos or player.direction.x >= 0)):
            player.onLeft = False;
        if(player.onRight and (player.rect.right > self.lastCollisionXPos or player.direction.x <= 0)):
            player.onRight = False;
    
    def VerticalMovementCollision(self):
        player = self.player.sprite;
        player.ApplyGravity();
    
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if(player.direction.y > 0):
                    player.rect.bottom = sprite.rect.top;
                    player.direction.y = 0;
                    player.onGround = True;
                elif(player.direction.y < 0):
                    player.rect.top = sprite.rect.bottom;
                    player.direction.y = 0;
                    player.onCeiling = True;
        if(player.onGround and player.direction.y < 0 or player.direction.y > 1):
            player.onGround = False;
        if(player.onCeiling and player.direction.y > 0):
            player.onCeiling = False;
    def run(self):
        # Dust particles
        self.dustSprite.update(self.worldShift);
        self.dustSprite.draw(self.displaySurf);

        # Level Tiles
        self.tiles.update(self.worldShift);
        self.tiles.draw(self.displaySurf);
        self.ScrollX();

        # Player
        self.player.update();
        self.HorizontalMovementCollision();
        self.GetPlayerOnGround();
        self.VerticalMovementCollision();
        self.CreateLandingDust();
        self.player.draw(self.displaySurf);
