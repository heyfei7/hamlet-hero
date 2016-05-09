#-------------------------------------------------------------------------------
# Name:        Wool World
# Purpose:     Mini game where player guides sheep into their pen
# Author:      Anya, 322088089
# Created:     24/05/2015
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from pygame.locals import *
pygame.init()
import time
from random import randrange
from math import sqrt

wScreen, hScreen = 800, 600
screen = pygame.display.set_mode((wScreen, hScreen))

bgfill = (34,177,76)                                                            #background fill colour is light green
sheepsize = 50

pensize = 200                                                                   #place pen, no matter the size, in the center of the screen
penleft, penwidth = (wScreen-pensize)/2, pensize
pentop, penheight = (hScreen-pensize)/2, pensize

def eraser(x,y,w,h):                                                            #erases previous sprite blit of the sheep, so that it doesn't leave traces
    erase = pygame.Surface((w,h)).convert()
    erase.fill(bgfill)
    screen.blit(erase,(x,y))

def printext(text,size, x,y):                                                   #displays a text on the screen
    font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", size)
    prntxt = font.render(text,1,(255,255,255))
    txtrect = prntxt.get_rect()

    screen.blit(prntxt,(x,y))

class woolPen(pygame.sprite.Sprite):                                            #pen into which all the sheep are herded
      def __init__(self,size):
          pygame.sprite.Sprite.__init__(self)

          self.image = pygame.image.load("wool\\wool pen.png").convert()
          self.image = pygame.transform.scale(self.image,(pensize,pensize))     #scale image to instructed size
          self.rect = self.image.get_rect()

      def refresh(self,pos):
          screen.blit(self.image,pos)

class woolSheep(pygame.sprite.Sprite):
      def __init__(self):
          pygame.sprite.Sprite.__init__(self)

          self.image = pygame.image.load("wool\\sheep.png").convert()
          transColor = self.image.get_at((0,0))
          self.image.set_colorkey(transColor)
          self.image = pygame.transform.scale(self.image,(sheepsize,sheepsize))
          self.rect = self.image.get_rect()

          self.speed = 1                                                        #set speed to 1 initially
          self.dirx, self.diry = randrange(-1,3,2), randrange(-1,3,2)           #determine initial direction randomly

          corners = {"1":(self.rect.width,self.rect.height),"2":(self.rect.width,hScreen-2*self.rect.height),"3":(wScreen-2*self.rect.width,self.rect.height),"4":(wScreen-2*self.rect.width,hScreen-2*self.rect.height)}
          rancorner = randrange(1,5)                                            #set sheep up in a random corner of the screen
          self.initpos = corners[str(rancorner)]
          self.rect.right,self.rect.top = self.initpos[0], self.initpos[1]

      def dir(self,mouse):                                                      #using positions of cursor and sheep, determines sheep's movement's direction
          if mouse[0] < self.rect.right:                                        #sheep moves AWAY from the cursor, if it's not on the sheep rect
             self.dirx = 1
          elif mouse[0] > self.rect.left:
               self.dirx = -1
          else:
               self.dirx = 0                                                    #if cursor is on the sheep rect, however, sheep doesn't move
          if mouse[1] < self.rect.top:
             self.diry = 1
          elif mouse[1] > self.rect.bottom:
                self.diry = -1
          else:
                self.diry = 0

      def move(self,mouse):                                                     #adjusting sheep's speed and direction, and moving it to new location
          distance = sqrt((self.rect.right - mouse[0])**2 + (self.rect.top - mouse[1])**2)
          maxeffect,noeffect, scale = 20,200, 50
          maxspeed,minspeed = 4,1

          #determine speed
          if distance < maxeffect:
             #if distance between mouse and sheep is less than 20, sheep moves at max speed, 4
             self.speed = maxspeed
             self.dir(mouse)
          elif maxeffect < distance < noeffect: #gradation of speed (1 to 4) depending on proximity of cursor
               self.speed = minspeed+(distance-maxeffect)*((maxspeed-minspeed)/(noeffect-maxeffect))
               self.dir(mouse)
          else: #distance between sheep and mouse is greater than 200; sheep moves wherever it wants, with normal speed, 1
                self.speed = 1
                ranroute = randrange(0,80)
                if ranroute == 30:
                   self.dirx *= -1
                elif ranroute == 40:
                     self.diry *= -1
                #else, sheep continues moving in exact same direction

          l,r,t,b = self.rect.left, self.rect.right, self.rect.top, self.rect.bottom
                                                                                #shortcuts to make checking up on rect attributes easier
          xsp,ysp = self.dirx*self.speed, self.diry*self.speed                  #more shortcuts

          #determine if direction needs to be changed
          while (0 > l+xsp or r+xsp > wScreen or 0 > t+ysp or b+ysp > hScreen):
##                print ("is there a problem?")
                if 0 > l+xsp or r+xsp > wScreen:
                   self.dirx *= -1
                if 0 > t+ysp or b+ysp > hScreen:
                   self.diry *= -1
                xsp,ysp = self.dirx*self.speed, self.diry*self.speed            #update direction and speed

          eraser (self.rect.left,self.rect.top,self.rect.width,self.rect.height)#erase old image of sheep
          self.rect.move_ip(xsp,ysp)

          screen.blit(self.image,(self.rect.left,self.rect.top))                #blit new image of sheep
          pygame.display.flip()

def woolStart():
    pygame.display.set_caption("Wool World")
    image = pygame.image.load("wool\\wool start screen.png").convert()
    screen.blit(image, (0,0))
    printext("Drive the fluffballs FULLY into the pen.",35, 60,400)
    printext("Without you, they wander.",35, 60,450)
    printext("Use your cursor - they're scared of it!",35, 60,500)
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

def woolGame(level):
    clock = pygame.time.Clock()
    clock.tick(10)                                                              #set frame rate to 10 frames per second
    start = time.time()

    bg = pygame.Surface((wScreen, hScreen)).convert()
    bg.fill(bgfill)
    screen.blit(bg,(0,0))                                                       #set background as light green

    shGroup = pygame.sprite.Group()
    for sheep in range(level):
        sh = woolSheep()                                                        #create sheep in accordance to the level
        shGroup.add(sh)

    pen = woolPen(pensize)
    pen.refresh((penleft,pentop))

    kg = True
    start = time.time()
    while kg:
          pygame.event.clear()
          pen.refresh((penleft,pentop))

          for sh in shGroup:
              sh.move(pygame.mouse.get_pos())
              pygame.display.flip()

              if penleft < sh.rect.left and sh.rect.right < penleft+penwidth and pentop < sh.rect.top and sh.rect.bottom < pentop+penheight:
                 shGroup.remove(sh)
                 eraser(sh.rect.left,sh.rect.top,sh.rect.width,sh.rect.height)
                 pen.refresh((penleft,pentop))

          if shGroup.sprites() == []:
             end = time.time()
             kg = False

    timespent = end-start
    score = 250*level/timespent                                                 #the longer the player takes to herd the sheep, the lower their score
    if score > 50:                                                              #score capped at 50
       score = 50
    else:
         score = int(score)                                                     #else, score will be rounded down to nearest integer

    return score

def woolEnd(score):
    end = pygame.image.load("wool\\wool end screen.png").convert()
    screen.blit(end,(0,0))
    printext(str(score),100, 450,425)                                           #print the score
    pygame.display.flip()

def wool(level):
    woolStart()
    score = woolGame(level)
    woolEnd(score)
    time.sleep(5)
    return score