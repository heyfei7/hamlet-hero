#-------------------------------------------------------------------------------
# Name:        Berrilicious
# Purpose:
#
# Author:      Fei Dong, 333845014
#
# Created:     10/04/2015
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from pygame.locals import *
pygame.init()

import time
import random

wScreen, hScreen = 800, 600                                                     #this is the screen
screen = pygame.display.set_mode((wScreen, hScreen))
pygame.display.set_caption("Hamlet Hero by Anya & Fei")

def printWord(text, color, x, y, size):                                         #if x or y = zero, then the text displays at the center of the x/y axis
    font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", size)
    text = font.render(text, False, color)
    textRect = text.get_rect()
    textRect.center = screen.get_rect().center
    if x != 0:
        textRect.left = x
    if y != 0:
        textRect.top = y
    screen.blit(text, textRect)

class berryCard(pygame.sprite.Sprite):                                          #this class decides the card
    def __init__(self, berry):
        pygame.sprite.Sprite.__init__(self)
        self.berry = berry
        self.image = self.image = pygame.image.load("berry\\berry back.png").convert()
        self.rect = self.image.get_rect()
        self.side = "back"

    def position(self, top, left):                                              #this defines the card's position
        self.rect.top = top
        self.rect.left = left

    def flip(self):                                                             #this flips the card between front (berry side) or back (uniform side)
        if self.side == "back":
            self.image = pygame.image.load("berry\\berry " + self.berry + ".png").convert()
            self.side = "berry"
        else:
            self.image = pygame.image.load("berry\\berry back.png").convert()
            self.side = "back"

    def done(self):                                                             #this shows when the card has been matched, a glowing pink outline appears
        self.image = pygame.image.load("berry\\berry " + self.berry + " done.png").convert()

def berryAllCards(listOfBerries, nOfPairs):                                     #this determines the cards in play
    listOfCards = list()
    yup = listOfBerries[:nOfPairs]
    for b in yup:
        b1 = berryCard(b)
        b2 = berryCard(b)
        listOfCards.append(b1)
        listOfCards.append(b2)
    random.shuffle(listOfCards)
    return listOfCards

def berryLayout(listOfBerries, nOfPairs):                                       #this determins the layout of the cards depending on number of cards
    listOfCards = berryAllCards(listOfBerries, nOfPairs)
    if nOfPairs >= 2 and nOfPairs <= 4:
        row1 = listOfCards[:len(listOfCards)//2]
        row2 = listOfCards[len(listOfCards)//2:]
        return [row1, row2]
    elif nOfPairs == 7:
        row1 = listOfCards[:4]
        row2 = listOfCards[4:9]
        row3 = listOfCards[9:]
    elif nOfPairs >= 5 and nOfPairs <= 8:
        row1 = listOfCards[:len(listOfCards)//3]
        row2 = listOfCards[len(listOfCards)//3:(len(listOfCards)//3)*2]
        row3 = listOfCards[(len(listOfCards)//3)*2:]
    return [row1, row2, row3]

def berryStart():                                                               #this is the start screen
    startScreen = pygame.image.load("berry\\berry start screen.png").convert()
    screen.blit(startScreen,(0,0))
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

def berryGame(listOfBerries, nOfPairs):                                         #this is the whole game
    background = pygame.image.load("berry\\berry background.png").convert()
    cards = berryLayout(listOfBerries, nOfPairs)
    kg = True

    clock = pygame.time.Clock()
    start = int(time.time())

    flipped = list()
    matched = 0

    while kg:
        screen.blit(background,(0,0))

        clock.tick(30)
        end = int(time.time())
        timePassed = end-start

        if pygame.event.peek(QUIT) == True:                                     #checks for the event quit
            pygame.display.quit()
            pygame.mixer.music.stop()
            quit()
        if timePassed > 1:
            for ev in pygame.event.get():                                           #checks for mouse button pressed
                if ev.type == MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    for row in allPos:                                              #for every row of cards
                        for card in row:                                            #for every card in row
                            if x >= card[1] and x <= card[1]+100 and y >= card[2] and y <= card[2]+150: #if the mouse is pressed on that card
                                if card[0].side == "back" and len(flipped) < 2:
                                    card[0].flip()                                  #flip the card
                                    flipped.append(card[0])

        allPos = list()                                                         #this determines all the cards and what they look like
        for row in cards:
            rowPos = list()
            for card in row:
                n,i1,r, i2 = len(row), row.index(card), len(cards), cards.index(row)
                top = (600-r*150)//(r+1)*(i2+1)+150*i2
                left = (800-100*n)//(n+1)*(i1+1)+100*i1
                rowPos.append([card,left,top])
                card.position(top, left)
                screen.blit(card.image, card.rect)
            allPos.append(rowPos)

        printWord("Time: "+str(timePassed), (157,145,169), 5, 5, 40)

        pygame.display.flip()

        if len(flipped) == 2:                                                   #if two cards are flipped
            if flipped[0].berry == flipped[1].berry:                            #and the two cards are the same, then they're matched
                matched += 1
                flipped[0].done()
                flipped[1].done()
                flipped = list()
                pygame.display.flip()
            else:                                                               #if they're not the same, flip them back
                time.sleep(0.5)
                flipped[0].flip()
                flipped[1].flip()
                flipped = list()

            if matched == nOfPairs:                                             #if matched all the cards, then the game is done
                time.sleep(1)
                kg = False

    return timePassed

def berryEnd(score):                                                            #end screen displays results
    endScreen = pygame.image.load("berry\\berry end screen.png").convert()
    screen.blit(endScreen,(0,0))
    printWord(str(score), (73,53,93), 495, 270, 150)
    printWord(str(score), (157,145,169), 500, 275, 150)
    pygame.display.flip()

def berry(level):                                                               #this executes the entire game
    berryStart()
    listOfBerries = ["blueberry","strawberry","raspberry","blackberry","cranberry","barberry","gooseberry","honeyberry"]
    timePassed = berryGame(listOfBerries,2*level+3)
    if timePassed <= 15:
        score = 50
    elif timePassed <= 20:
        score = 45
    elif timePassed <= 30:
        score = 40
    elif timePassed <= 45:
        score = 35
    else:
        score = 30

    berryEnd(score)
    time.sleep(5)
    return score