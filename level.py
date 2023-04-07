import pygame
from tiles import Tile;
from settings import tileSize;
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
    
    def run(self):
        # Level Tiles
        self.tiles.update(self.worldShift);
        self.tiles.draw(self.displaySurf);

        # Player
        self.player.update();
        self.player.draw(self.displaySurf);