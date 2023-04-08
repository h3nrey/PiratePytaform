from os import walk
import pygame

def ImportFolder(path):
    surfs = []
    for _, _, imgFiles in walk(path):
        for fileName in imgFiles:
            fullPath = path + "/" + fileName;
            print(fullPath);
            img = pygame.image.load(fullPath).convert_alpha();
            surfs.append(img);
    return surfs;

