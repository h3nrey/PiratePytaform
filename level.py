import pygame, math
from tiles import Tile;
from settings import tileSize, screenW, camBorder;
from player import Player;

class Level:
    def __init__(self, levelData, surface):
        self.displaySurf = surface;
        self.setupLevel(levelData);
        self.worldShift = 0;

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
                    playerSpr = Player((x,y));
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

    def HorizontalMovementCollision(self):
        player = self.player.sprite;
        player.rect.x += player.direction.x * player.speed;
    
        for sprite in self.tiles.sprites():
            if(sprite.rect.colliderect(player.rect)):
                if(player.direction.x < 0):
                    player.rect.left = sprite.rect.right;
                elif(player.direction.x > 0):
                    player.rect.right = sprite.rect.left;
    
    def VerticalMovementCollision(self):
        player = self.player.sprite;
        player.ApplyGravity();
    
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if(player.direction.y > 0):
                    player.rect.bottom = sprite.rect.top;
                    player.direction.y = 0;
                elif(player.direction.y < 0):
                    player.rect.top = sprite.rect.bottom;
                    player.direction.y = 0;
    def run(self):
        # Level Tiles
        self.tiles.update(self.worldShift);
        self.tiles.draw(self.displaySurf);
        self.ScrollX();

        # Player
        self.player.update();
        self.HorizontalMovementCollision();
        self.VerticalMovementCollision();
        self.player.draw(self.displaySurf);
