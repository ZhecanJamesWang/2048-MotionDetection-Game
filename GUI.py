################################################################################################################
# Package Imports                                                                                              #
################################################################################################################
import pygame
import random
from pickle import dump,load
import time
import math
import sys
import os
from pygame.locals import *
from math import *
# import face_detection_2048_sub
from game_2048 import *
# from game2048_face_detectionfunc import*
# from game_2048_text_version.py import *

################################################################################################################
# Global Variable Definitions                                                                                  #
################################################################################################################
clock = pygame.time.Clock()
pygame.font.init()
tileList = []

# font initialization
scorefont = pygame.font.SysFont('Ariel', 50, bold=True, italic=False)
titlefont = pygame.font.SysFont('Ariel', 40, bold=True, italic=False)
GameOver = pygame.font.SysFont('Ariel', 140, bold=True, italic=False)
font = pygame.font.SysFont('Ariel', 80, bold=True, italic=False)

# Color Definitions
WHITE = (255, 255, 255)
GREY = (119, 136, 153)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# screen size
screenWidth = 600
screenHeight = 700

# calculate tile size
tileW = screenWidth/5
tileH = (screenHeight-100)/5

# calculate tile spacing
xSpace = tileW/5
ySpace = tileH/5
xTiles = 4
yTiles = 4
Tiles = xTiles*yTiles

# start points at 0
points=0

################################################################################################################
# Class Definitions                                                                                            #
################################################################################################################

################################################################################################################
# Class Definitions                                                                                            #
################################################################################################################

class Background():  # represents the player, not the game
    def __init__(self,color,width,height):
        """ The constructor of the class """
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # the background's position
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0

    def draw(self, surface):
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))


class Tile():  # represents the player, not the game
    def __init__(self,color,width,height,x,y,val=0):
        """ The constructor of the class """
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # the tile's position
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.val = val

    def getColor(self):
        # calculate the color of the passed in tile
        x = self.val
        if x == 0:
            hue = (200,200,200)
        else:
            hue = (255/sqrt(x),0,0)
        return hue

    def showValue(self,x,y,w,h):
        # find and then print the value of each tile
        tileVal = self.val
        # if 0 dont print anything
        if tileVal == 0:
            pass
        else:
            # otherwise print the value centered on the tile
            val = str(tileVal)
            label = font.render(val,True,(255,255,255))
            labelRect = label.get_rect()
            area = font.size(val)  
            labelRect.center = (x+w/2-area[0]/2, y+h/2-area[1]/2)
            screen.blit(label, (labelRect.center))

    def draw(self, surface):
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))

class Scorebox():  # represents the player, not the game
    def __init__(self,color,width,height,x,y,val=0):
        """ The constructor of the class """
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # the box's position
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # self.val = val

    def draw(self, surface):
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))


def generateTiles(tileNumber,xtiles,ytiles,width,height,xspace,yspace,alist):
    # del tileList[:]
    for col in range(xtiles):
        for row in range(ytiles):
            baseColor = (WHITE)
            # create base tile
            tile = Tile(baseColor, width, height, 0, 0, alist[col][row])
            # get new tile info
            c = tile.getColor()
            x = xspace*col + width*col + xspace
            y = yspace*row + height*row + yspace
            # create new tile
            newtile = Tile(c, width, height, x, y, alist[row][col])
            # print the tile
            newtile.draw(screen)
            tile.showValue(x,y,width,height)
            # tileList.append(newtile)

def boxTitles(xspace,yspace):
    # create objects for titles
    curScore = titlefont.render('Current Score',True,(255,255,255))
    highScore = titlefont.render('High Score',True,(255,255,255))
    # find position for the titles
    curscoreRect = curScore.get_rect()  
    area1 = titlefont.size('Current Score')
    curscoreRect.center = (xspace+((screenWidth-4*xspace)/4)-area1[0]/2 + xspace/2, 600)
    highscoreRect = highScore.get_rect()  
    area2 = titlefont.size('High Score')
    highscoreRect.center = (3*xspace+((screenWidth-4*xspace)/4)-area2[0]/2 + (screenWidth-4*xspace)/2 - xspace/2, 600)
    # print titles
    screen.blit(curScore, (curscoreRect.center))
    screen.blit(highScore, (highscoreRect.center))

def showScoreboxes(xspace,yspace):
    color = (100,100,100)
    y = screenHeight-100
    width = (screenWidth-4*xspace)/2 + xspace/2
    height = 100 - yspace
    curScorebox = Scorebox(color,width,height,xspace,y)
    screen.blit(curScorebox.image, (curScorebox.x,curScorebox.y))
    highScorebox = Scorebox(color,width,height,2*xspace+width,y)
    screen.blit(highScorebox.image, (highScorebox.x,highScorebox.y))
    boxTitles(xspace,yspace)

def findScore(alist,xtiles,ytiles):
    # find the score in the game so far by iterating
    # through the matrix of values and adding them
    score = 0
    for i in range(xtiles):
        for j in range(ytiles):
            score = score + alist[i][j]
    return score

def printScore(alist,xtiles,ytiles,xspace, yspace):
    # print the score so far
    pointsStr = str(findScore(alist,xtiles,ytiles))
    # create a object of the score
    score = scorefont.render(pointsStr,True,(255,255,255))
    # score = scorefont.render(pointsStr,True,(255,255,255))
    # find position for the score
    scoreRect = score.get_rect()  
    area = font.size(pointsStr)
    scoreRect.center = (150 - area[0]/2 + xspace/2, 625+(50-yspace/2-area[1]/2))
    # print score
    screen.blit(score, (scoreRect.center))

def printHighScore(alist,xtiles,ytiles,xspace,yspace):
    # print highscore
    pointsStr = str(findHighScore(alist))
    # create a object of the score
    score = scorefont.render(pointsStr,True,(255,255,255))
    # find position for the score
    scoreRect = score.get_rect()  
    area = font.size(pointsStr)
    scoreRect.center = (4*xspace + 3*(screenWidth-4*xspace)/4 - area[0]/2 - xspace/2, 625+(50-yspace/2-area[1]/2))
    # print score
    screen.blit(score, (scoreRect.center))

def printEnd():
    # print game over
    pointsStr = 'Game Over'
    # create a object of the score
    score = scorefont.render(pointsStr,True,(255,0,0))
    # find position for the score
    scoreRect = score.get_rect()  
    area = font.size(pointsStr)
    # scoreRect.center = (screenWidth/2 - area[0]/2, (screenHeight-100)/2-area[1]/2)
    scoreRect.center = (0,0)
    # print score
    screen.blit(score, (scoreRect.center))

def loadScores():
    filename = './scores.txt'
    data_file = open(filename,'r')
    scorelist = load(data_file)
    data_file.close()
    return scorelist

def saveScore(alist,blist,xtiles,ytiles):
    finalscore = findScore(blist,xtiles,ytiles)
    alist.append(finalscore)
    filename = './scores.txt'
    data_file = open(filename,'w')
    dump(scoreList,data_file)
    data_file.close()

def findHighScore(alist):
    return max(alist)

def end_game(event):
    # for event in pygame.event.get():
    if event.type == pygame.QUIT:
        sys.exit() # quit the screen
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            sys.exit() # quit the screen

def end():
    comi = raw_input()
    if comi == 'q':
        sys.exit()
    else:
        #If did not enter valid key, notify user and ask for input again
        print("Not a valid move")

################################################################################################################
# Final Initialization                                                                                         #
################################################################################################################

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))

################################################################################################################
# Run Main Loop                                                                                                #
################################################################################################################

olist=[[0]*4,[0]*4,[0]*4,[0]*4]
background = Background(WHITE,screenWidth,screenHeight)
# saveScore(scoreList,xTiles,yTiles)
scoreList = loadScores()
findHighScore(scoreList)

# if __name__=="__main__":

def game_2048_text_version(command):
    # print "5"
    global olist
    #Add in random 2 (if space available)
    update = rand_add(olist) #?????????????

    
    
    olist = update[0]
    
    if update[1]:
        #If moves still available, keep game going
        olist=run_command(olist,command)
        background.draw(screen)
    
        generateTiles(Tiles,xTiles,yTiles,tileW,tileH,xSpace,ySpace,olist)
        showScoreboxes(xSpace,ySpace)
        printScore(olist,xTiles,yTiles,xSpace,ySpace)
        printHighScore(scoreList,xTiles,yTiles,xSpace,ySpace)
        pygame.display.flip()

    else:
        # print("final points", points)
        print("****Game Over****")
        while 1:
            background.draw(screen)
            generateTiles(Tiles,xTiles,yTiles,tileW,tileH,xSpace,ySpace,olist)
            showScoreboxes(xSpace,ySpace)
            printEnd()
            printScore(olist,xTiles,yTiles,xSpace,ySpace)
            printHighScore(scoreList,xTiles,yTiles,xSpace,ySpace)
            end()




