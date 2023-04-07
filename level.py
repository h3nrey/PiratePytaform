import pygame
from tiles import Tile;
from settings import tileSize;

class Level:
    def __init__(self, levelData, surface):
        self.displaySurf = surface;
        self.setupLevel(levelData);
        self.worldShift = 0;

    def setupLevel(self, layout):
        self.tiles = pygame.sprite.Group();

        for rowIndex, row in enumerate(layout):
            for cellIndex, cell in enumerate(row):
                x, y = cellIndex * tileSize, rowIndex * tileSize;
                if(cell == "X"): 
                    tile = Tile((x,y), tileSize)
                    self.tiles.add(tile);
    
    def run(self):
        self.tiles.update(self.wordlShift);
        self.tiles.draw(self.displaySurf);