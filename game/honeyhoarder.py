#-------------------------------------------------------------------------------
# Name:        Honey Hoarder
# Purpose:     Mini game where the player click on the bees in order to catch them
# Author:      Anya, 322088089
# Created:     10/04/2015
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from pygame.locals import *
pygame.init()
import time
from random import randrange

wScreen, hScreen = 800, 600
screen = pygame.display.set_mode((wScreen, hScreen))

bgfill = (255,255,213)                                                          #background fill colour is light yellow

beesize = 50

def eraser(x,y,w,h):                                                            #erases previous sprite blit of a bee, so that it doesn't leave traces
    erase = pygame.Surface((w,h)).convert()
    erase.fill(bgfill)
    screen.blit(erase,(x,y))

def printext(text,size, x,y):                                                   #displays a text on the screen
    font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", size)
    prntxt = font.render(text,1,(0,0,0))
    txtrect = prntxt.get_rect()

    if x == "c":
       txtrect.centerx = screen.get_rect().centerx
    else:
         txtrect.left = x
    if y == "c":
       txtrect.centery = screen.get_rect().centery
    else:
         txtrect.top = y

    screen.blit(prntxt,txtrect)

class honeyBee(pygame.sprite.Sprite):
      def __init__(self):                                                       #initialize the bee's image and its starting flight direction
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("honey\\honey bee.png").convert()
        transColor = self.image.get_at((0,0))
        self.image.set_colorkey(transColor)
        self.image = pygame.transform.scale(self.image,(beesize,beesize))
        self.rect = self.image.get_rect()

        directx = randrange(0,2)                                                #set initial direction for bee's flight randomly
        if directx == 0:
           self.directionx = -1 #goes left
        else: #directx == 1
             self.directionx = 1 #goes right
        directy = randrange(0,2)
        if directy == 0:
           self.directiony = -1 #goes up
        else: #directy == 1
             self.directiony = 1 #goes down

      def letter(self,letter):                                                  #stamp the bee's letter onto its image and save the letter for future recall
          self.let = letter
          letter = letter.upper() #all letters should be upper case
          font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 30)
          prntxt = font.render(letter,1,(255,0,255))#(255,255,255))
          txtrect = prntxt.get_rect()
          self.image.blit(prntxt,(self.image.get_rect().centerx - txtrect.centerx,self.image.get_rect().centery - txtrect.centery))

      def initPos(self,initpos):                                                #set the bee's coordinates as the ones randomly generated in main program
          self.rect.left, self.rect.top = initpos[0], initpos[1]

      def fly(self,level,index,bGroup):
          speed = level#**2                                                     #the bee's speed will depend on the level; moreover, the less bees left to catch, the faster it goes
          l,r,t,b = self.rect.left, self.rect.right, self.rect.top, self.rect.bottom
                                                                                #shortcuts to make checking up on rect attributes easier

          rndm = randrange(0,8)                                                 #determine randomly whether bee will change directions
          if rndm == 3:
             self.directionx *= -1
          elif rndm == 4:
             self.directiony *= -1
          #else: bee keeps flying in same exact direction

          xsp,ysp = self.directionx*speed, self.directiony*speed                #more shortcuts

          if pygame.sprite.spritecollideany(self,bGroup) != self:               #if bee is colliding with another bee,
             self.directionx *= -1
             self.directiony *= -1                                              #full direction reversal

          if (0 > l+xsp or r+xsp > wScreen or 0 > t+ysp or b+ysp > hScreen):
          #if bee wouldn't be in bounds of the screen with its current direction, change it
                 if 0 > l+xsp or r+xsp > wScreen:                               #if bee's x position would be outside left or right side of game window,
                    self.directionx *= -1                                       #reverse it
                 if 0 > t+ysp or b+ysp > hScreen:                               #if bee's y position would be outside top or bottom of game window,
                     self.directiony *= -1                                      #reverse it

                 xsp,ysp = self.directionx*speed,self.directiony*speed          #updating direction and speed

          eraser (l,t,self.rect.width,self.rect.height)                         #erase bee in old position
          self.rect.move_ip(xsp,ysp)

          screen.blit(self.image,(self.rect.left,self.rect.top))                #blit bee in new position
          pygame.display.flip()

      def returnLetter(self):
          return self.let

      def die(self):
          eraser(self.rect.left,self.rect.top,self.rect.width,self.rect.height)
          screen.blit(self.image,(wScreen+1000,hScreen+1000))

def honeyWordpick(level):                                                       #chooses a random word, according to level difficulty, for the game instance
    #theme: sweet things
    #level 1 - 5-7 letters
    #level 2 - 8-10 letters
    #level 3 - 11-13 letters (if we need it)
    words = {"beehive":1,"nectar":1,"praline":1, "drone":1, "sweet":1,
            "hivemind":2,"fructose":2,"fireweed":2,"hydromel":2,"honeybird":2
            ,"mellifluent":3} #don't need level 3..

    wordlist = list()
    for w,l in words.items():
        if l == level:
           wordlist.append(w)
    ranpick = randrange(0,len(wordlist))
    word = wordlist[ranpick]

    return word

def honeyBeeletter(word):                                                       #adds a sprite (bee) to group to represent each letter in given word
    bGroup = pygame.sprite.Group()
    for index in range(len(word)):
        b = honeyBee()
        b.letter(word[index])
        bGroup.add(b)

    return bGroup

def honeyStart(word):
    pygame.display.set_caption("Honey Hoarder")
    image = pygame.image.load("honey\\honey start screen short.png").convert()
    screen.blit(image, (0,0))
    printext("The word is %s."%word,70, 50,250)
    printext("The word will remain as the window's caption.",30, 50,350)
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

def honeyGame(level,word):
    pygame.display.set_caption(word)
    bg = pygame.Surface((wScreen, hScreen)).convert()
    bg.fill(bgfill)
    screen.blit(bg,(0,0))

    bGroup = honeyBeeletter(word)                                               #give word for creating group of bee sprites
    for index in range(len(word)):
        b = bGroup.sprites()[index]                                             #pull specific bee sprite from the group
        randpos = (randrange(0,wScreen-beesize), randrange(0,hScreen-beesize))  #randomly place it on the screen
        while pygame.sprite.spritecollideany(b,bGroup) != b:
              randpos = (randrange(0,wScreen-beesize), randrange(0,hScreen-beesize))
        screen.blit(b.image,randpos)
        b.initPos(randpos)                                                      #save bee's initial position
        pygame.display.flip()

    wordcom = list()
    for i in range(len(word)):
        wordcom.append(word[i])

    clock = pygame.time.Clock()
    clock.tick(50)                                                              #set frame rate to 50 frames per second
    start = time.time()
    kg = True

    while kg:
          for ev in pygame.event.get():                                         #if player wants to exit window,
              if ev.type == QUIT:
                 pygame.display.quit()
                 pygame.quit()                                                  #exit everything

              elif ev.type == MOUSEBUTTONDOWN:                                  #if player clicks their mouse,
                 mxny = pygame.mouse.get_pos()                                  #get mouse coordinates
                 for b in bGroup:                                               #check them against each bee in sprite group
                     if b.rect.collidepoint(mxny):
                        if b.returnLetter() == wordcom[0]:                      #if the mouse is in the bee's rectangle and that bee's letter is the first of the remaining letters in the word,
                           print ("Good job, that was the right bee.")
                           b.die()                                              #remove bee from screen,
                           bGroup.remove(b)                                     #group,
                           del wordcom[0]                                       #and its letter from the list
                        else:
                             print ("Sorry, wrong bee.")
                     else:
                          print ("Sorry, no bee.")

          end = time.time()
          if len(wordcom) == 0 or end-start > 30:                               #if they catch all the bees or 30 seconds have passed,
             kg = False                                                         #the mini-game is over

          for index in range(len(wordcom)):
              b = bGroup.sprites()[index]
              b.fly(level,index,bGroup)
              pygame.display.flip()

    timespent = end-start
    score = 50*len(word)*level/timespent                                        #the longer the player takes to catch all the bees, the lower their score
    if score > 50:                                                              #score capped at 50
       score = 50
    elif float(str(score)[2:]) >= 0.5:                                          #Python always rounds down when making a float an integer, which, in this case, makes for worse user experience
         score = int(score)+1                                                   #This allows the player to get a fairer score for the minigame instance
    else:
         score = int(score)

    return score

def honeyEnd(score):
    end = pygame.image.load("honey\\honey end screen.png").convert()
    screen.blit(end,(0,0))
    printext(str(score),60, 550,490)                                            #print the score with same hot pink background as on end screen
    pygame.display.flip()

def honey(level):
    word = honeyWordpick(level)
    honeyStart(word)
    score = honeyGame(level,word)
    honeyEnd(score)
    time.sleep(5)
    return score