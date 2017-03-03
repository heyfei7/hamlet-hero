#-------------------------------------------------------------------------------
# Name:        Metal Miner
# Purpose:
#
# Author:      Anya Pechkina and Fei Dong
#
# Created:     27/03/2015
#-------------------------------------------------------------------------------
#!/usr/bin/env python

"""slightly darker background for the character"""

import pygame
from pygame.locals import *
pygame.init()

import time
import random

wScreen, hScreen = 800, 600                                                     #this is the screen
screen = pygame.display.set_mode((wScreen, hScreen))

def printWord(text, x, y, size):                                                #if x or y = zero, then disregard it
    font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", size)
    text = font.render(text, False, (255,255,255))
    textRect = text.get_rect()
    textRect.center = screen.get_rect().center
    if x != 0:
        textRect.left = x
    if y != 0:
        textRect.top = y
    screen.blit(text, textRect)


class metalWall(pygame.sprite.Sprite):                                          #this class decides the wall
    def __init__(self,wPos,lr, speed):
        pygame.sprite.Sprite.__init__(self)
        if lr == "left":
            self.image = pygame.image.load("metal\\metal wall left.png").convert()
        elif lr == "right":
            self.image = pygame.image.load("metal\\metal wall right.png").convert()

        self.rect = self.image.get_rect()

        self.speed = speed

    def moveDown(self, hpos):
        self.rect.top = hpos

class metalPerson(pygame.sprite.Sprite):                                        #this class decides the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("metal\\metal character.png").convert()
        self.rect = self.image.get_rect()

        self.rect.centerx = 400
        self.rect.top = 500

    def moveLeft(self):
        self.rect.move_ip(-15,0)

    def moveRight(self):
        self.rect.move_ip(15,0) #x and then y

class metalObstacle(pygame.sprite.Sprite):                                      #these are the obstacles
    def __init__(self, gb, speed, time):
        pygame.sprite.Sprite.__init__(self)                                     #construct the parent component
        self.time = time
        if gb == "g":
            r = random.randrange(0,5)
            if r == 0:
                self.image = pygame.image.load("metal\\metal gem blue.png").convert()
            elif r == 1:
                self.image = pygame.image.load("metal\\metal gem red.png").convert()
            elif r == 2:
                self.image = pygame.image.load("metal\\metal gem green.png").convert()
            elif r == 3:
                self.image = pygame.image.load("metal\\metal gem orange.png").convert()
            else:
                self.image = pygame.image.load("metal\\metal gem purple.png").convert()
            self.type = gb
        elif gb == "b":
            self.image = pygame.image.load("metal\\metal rock.png").convert()
            self.type = gb
        self.rect = self.image.get_rect()
        wSize = self.image.get_size()[0]
        self.speed = speed

        self.rect.centerx = random.randrange(320,500-wSize-20)
        self.rect.top = 0

    def setSpeed(self, speed):
        self.speed = speed

    def moveDown(self):
        self.rect.move_ip(0, self.speed)

def metalTListGen():
    tList = list()
    for o in range(1,25):
        r = random.randrange(o, o+3)
        if not r in tList:
            tList.append(r)
    tList.sort()
    return tList

def metalStart():
    image = pygame.image.load("metal\\metal start screen.png").convert()
    screen.blit(image, (0,0))
    pygame.display.flip()
    button = pygame.image.load("replay\\next.png").convert()
    screen.blit(button, (590,10))
    pygame.display.flip()
    bnp = True
    while bnp:
          for ev in pygame.event.get():
              if ev.type == MOUSEBUTTONDOWN:
                 x,y = pygame.mouse.get_pos()
                 if 590 < x < 790 and 10 < y < 110:
                    bnp = False

def metalGame(speed):
    back = pygame.image.load("metal\\metal background.png").convert()
    bh = back.get_size()[1]
    hpos = bh*-1 + hScreen

    wall1 = metalWall(0, "left", speed)
    wall2 = metalWall(525, "right", speed)
    screen.blit(back, (0, hpos))
    screen.blit(wall1.image, (0, hpos))
    screen.blit(wall2.image, (525, hpos))
    pygame.display.flip()

    clock = pygame.time.Clock()
    kg = True
    start = time.time()

    person = metalPerson()                                                      #the person

    oGroup = pygame.sprite.Group()                                              #Create group of sprites which will, on collision with player, end the game
    rGroup = pygame.sprite.Group()

    tList = metalTListGen()
    oList = list()
    for t in tList:
        gb = random.randrange(0,6)
        if gb > 2:
            o = metalObstacle("g", speed, t)
            rGroup.add(o)                                                       #Add, if bad obstacle, to end-game trigger group
        else:
            o = metalObstacle("b", speed, t)
            oGroup.add(o)
        oList.append(o)

    oGroup.add(wall1)
    oGroup.add(wall2)

    score = 0

    while kg:

        end = time.time()                                                       #this shows the time passed since the game started
        timePassed = int(end-start)
        clock.tick(30)

        if timePassed == 30:
            return score

        hpos += speed
        screen.blit(back, (0, hpos))                                            #this blits the background and the wall at the right place
        wall1.moveDown(hpos)
        wall2.moveDown(hpos)
        screen.blit(wall1.image, (0, hpos))
        screen.blit(wall2.image, (525, hpos))

        if hpos + bh < hScreen:
            screen.blit(back, (0, hpos))
            screen.blit(wall1, (0, hpos))
            screen.blit(wall2, (525, hpos))
        elif hpos + bh > hScreen:
            screen.blit(back, (0, hpos))
            screen.blit(wall1.image, (0, hpos))
            screen.blit(wall2.image, (525, hpos))

            screen.blit(back, (0, hpos-2400))
            screen.blit(wall1.image, (0, hpos-2400))
            screen.blit(wall2.image, (525, hpos-2400))
            if hpos > 2400:
                hpos -= 2400

        if pygame.event.peek(QUIT) == True:                                     #checks for the event quit
            pygame.display.quit()
            pygame.mixer.music.stop()
            quit()
        for ev in pygame.event.get():                                           #checks for left or right key
            if ev.type == KEYDOWN:
                if ev.key == K_LEFT:
                    person.moveLeft()
                    screen.blit(person.image, person.rect)
                elif ev.key == K_RIGHT:
                    person.moveRight()
                    screen.blit(person.image, person.rect)

        ghits = pygame.sprite.spritecollide(person, rGroup, True)               #check for collision
        if ghits != []:                                                         #aka good collision
            for o in oList:
                if o.type == "g":
                    oList.remove(o)
                    break
            score += 1
        bhits = pygame.sprite.spritecollide(person, oGroup, False)
        if bhits != [] or 275 >= person.rect.left or person.rect.right >= 525:  #aka bad collision
            printWord("Game Over", 0, 0, 40)
            pygame.display.flip()
            time.sleep(2)
            return score

        for o in oList:
            if o.time < timePassed:
                o.moveDown()
                screen.blit(o.image, o.rect)

        #this displays person
        screen.blit(person.image, person.rect)

        printWord("Time: " + str(30-timePassed), 5, 5, 40)
        printWord("Gem: " + str(score), 5, 40, 40)

        pygame.display.flip()

#this shows the end screen
def metalEnd(score):
    image = pygame.image.load("metal\\metal end screen.png").convert()
    screen.blit(image, (0,0))
    if score > 10:
       score = 10
    printWord(str(score), 580, 300, 100)
    pygame.display.flip()
    time.sleep(5)

def metal(level):
    metalStart()
    score = metalGame(5+level)
    metalEnd(score)
    return score