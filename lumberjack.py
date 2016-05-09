#-------------------------------------------------------------------------------
# Name:        LumberJack
# Purpose:     Mini game where player uses arrows to fell a tree
# Author:      Anya, 322088089
# Created:     28/04/2015
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from pygame.locals import *
pygame.init()
import time

wScreen, hScreen = 800, 600
screen = pygame.display.set_mode((wScreen, hScreen))

def printext(text,size, x,y, fill):                                             #displays a text on the screen
    font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", size)
    prntxt = font.render(text,1,(218,239,213),fill)
    txtrect = prntxt.get_rect()

    screen.blit(prntxt,(x,y))

def lumberMoveAxe(count,press,get,chop,treestage):
    plpos = (wScreen/2,hScreen/2)

    moveCor = ["l","r"]
    moveSteps = {"l":K_LEFT,"r":K_RIGHT}

    keypressed = False
    for ev in get:
        if ev.type == QUIT:
           pygame.display.quit()
           quit()
        elif ev.type == KEYDOWN:                                                #if key down, check which key
             if ev.key == moveSteps[moveCor[press%2]]:                          #if key is pressed in right order after last one (ie. left arrow after right arrow and vice versa)
                keypressed = True
                if ev.key == K_RIGHT and count%2!=0:                            #if key is "right arrow" and current player position counter doesn't already indicate "right",
                   count -= 1                                                   #change player position counter to indicate "right"
                if ev.key == K_LEFT and count%2!=1:                             #ditto with "left arrow"
                   count += 1

    if keypressed:
       press += 1
       #screen.blit(bg,(0,0))
       if count%2 == 0:
          rswing = pygame.image.load("lumber\\lumber %s%d p1.png" %treestage).convert() #change player image to correspond with position counter as "right"
          screen.blit(rswing,(0,0))
       else:                                                                    #change player image to correspond with position counter as "left"
            lswing = pygame.image.load("lumber\\lumber %s%d p3.png" %treestage).convert()
            screen.blit(lswing,(0,0))
            chop += 1                                                           #also, swing left means player has made a chop to the tree
       pygame.display.flip()

    return count,press,chop

def lumberStart():
    pygame.display.set_caption("LumberJack")
    image = pygame.image.load("lumber\\lumber start screen.png").convert()
    screen.blit(image, (0,0))
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

def lumberGame(level):
    clock = pygame.time.Clock()
    clock.tick(30)

    treeCor = {"1":"m","2":"l"} #corresponding letter of tree size, medium and large, to level
    treeStages = {"m":3,"l":4} #medium has 3 stages; large has 4
    treeChopLim = {"m":15,"l":20} #how many chops (or left swings) it takes to fell the tree

    tree = treeCor[str(level)]
    treeS, treeCL = treeStages[tree], treeChopLim[tree]

    kg = True
    imgcount,chop,press = 0,0,0
    stage = 1

    firstswing = pygame.image.load("lumber\\lumber %s1 p1.png" %tree).convert()         #start background image off with player in right swing position at
    screen.blit(firstswing,(0,0))
    pygame.display.flip()

    start = time.time()
    while kg:
          pygame.display.set_caption("LumberJack Time taken: %.1f s"%(time.time()-start))
                                                                                #let player know how many seconds have passed
##          pygame.event.clear()                                                  #clear pygame event cache, keeps game running smoothly
          if stage < treeS:
             if chop != 0:
                  stage = int(chop/treeCL*(level+1))                            #stage of the tree being chopped depends on the number of chops made
                  if stage == 0:
                     stage = 1
             imgcount,press,chop = lumberMoveAxe(imgcount,press,pygame.event.get(),chop,(tree,stage))
          else:
               kg = False
               end = time.time()
               #print final felled stage of tree? #no: no available visual...

    timespent = end - start
    score = 10*treeCL/(timespent*level**2)                                      #this minigame is cutthroat in terms of time
                                                                                #for level 2, to get the full 10 score, you need to do it under 5 seconds (it's possible, I've done it)
    if score > 10:                                                              #score capped at 10
       score = 10
    else:                                                                       #else, score will be rounded down to nearest integer
         score = int(score)

    return score

def lumberEnd(score):
    end = pygame.image.load("lumber\\lumber end screen.png").convert()
    screen.blit(end,(0,0))
    printext(str(score),80, 500,200, (101,78,57))                               #print the score with same light brown background as on end screen
    pygame.display.flip()

def lumber(level):
    lumberStart()
    score = lumberGame(level)
    lumberEnd(score)
    time.sleep(5)
    return score