#-------------------------------------------------------------------------------
# Name:        Boss Level
# Purpose:
#
# Author:      Fei Dong, 333845014
#
# Created:     29/04/2015
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

class bossBox(pygame.sprite.Sprite):                                            #this class defines the boxes, including attack, defense, and health bar
    def __init__(self, left, top, t):
        self.type = t
        self.boxLeft = left
        self.boxTop = top

        if self.type == "healthbarinside":
            self.box = pygame.Surface((360,40)).convert()
            self.color = (13,103,111)
            self.box.fill(self.color)
        else:
            self.box = pygame.image.load("boss\\boss " + str(self.type)+".png").convert()
        self.boxRect = self.box.get_rect()
        self.boxRect.topleft = ((self.boxLeft,self.boxTop))

    def changeWidth(self, newWidth):
        self.box = pygame.Surface((newWidth, self.boxRect.height)).convert()
        self.box.fill(self.color)

class bossPlayer(pygame.sprite.Sprite):                                         #this class defines the players, either the user or the cpu generated boss
    def __init__(self, defense, attack, health, cAttack, t, n):
        pygame.sprite.Sprite.__init__(self)
        self.type = t
        self.time = n
        if self.type == "me":
            self.defense = defense
            self.attack = attack
            self.health = health*2
            self.maxHealth = health*2
            self.cAttack = cAttack
        elif self.type == "boss":
            self.defense = 30*n-5*n
            self.attack = 20*n
            self.health = 200*n-10*(n)
            self.maxHealth = 240*n-10*(n)
            self.cAttack = 20*n

    def actionAttack(self, opponent):                                           #attacks the opponent with the final damage
        self.finalDamage = self.attack
        r = random.randrange(0,5)
        if r == 4:
            self.finalDamage += self.cAttack

        self.finalDamage = int(self.finalDamage - (opponent.defense/(100*self.time))*self.finalDamage)

        opponent.healthChange(-self.finalDamage)

    def actionDefense(self):                                                    #defends self against the opponent's attack
        if self.defense < 50*self.time:
            self.defense += 15

    def healthChange(self, change):                                             #changes health
        self.health += change

def printWord(text, color, x, y, size):                                         #if x or y = zero, then disregard it
    font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", size)
    text = font.render(text, False, color)
    textRect = text.get_rect()
    textRect.center = screen.get_rect().center
    if x != 0:
        textRect.left = x
    if y != 0:
        textRect.top = y
    screen.blit(text, textRect)

def bossAction():                                                               #determines whether or not the boss attacks or defends
    r = random.randrange(0,5)
    if r != 4:
        return "a"
    else:
        return "d"

def bossBackground(background, boxes):                                          #blits all of the attack/defense/health boxes and the background
    screen.blit(background, (0,0))
    for box in boxes:
        screen.blit(box.box, box.boxRect)

def bossPersonAttack(person, opponent, opponentHealthBarInside):                #if a Player is attacking, it decreases the oponnet's health and displays appropriate text
    person.actionAttack(opponent)
    if person.finalDamage > person.attack:
        printWord("Critical hit! The damage was "+str(person.finalDamage), (255,255,255), 0, 500, 35)
    else:
        if person.type == "me":
            printWord("You attacked! The damage was "+str(person.finalDamage), (255,255,255), 0, 500, 35)
        elif person.type == "boss":
            printWord("The boss attacked! The damage was "+str(person.finalDamage), (255,255,255), 0, 500, 35)
    newWidth = int(opponent.health/opponent.maxHealth*360)
    if newWidth <= 0:
        newWidth = 1
    opponentHealthBarInside.changeWidth(newWidth)

def bossStart():                                                                #shows the start screen
    background = pygame.image.load("boss\\boss background.png").convert()
    screen.blit(background,(0,0))

    instruction = ["Hello", "Welcome to the boss level.", "When it's your turn, choose attack or defense.", "Play to beat the boss."]

    for line in instruction:
        screen.blit(background,(0,0))
        printWord(line, (255,255,255), 0, 0, 35)
        pygame.display.flip()
        time.sleep(2)

def bossGame(score):                                                            #overall game
    background = pygame.image.load("boss\\boss regular.png").convert()
    screen.blit(background,(0,0))
    pygame.display.flip()

    defense = int(score["lumber"]+score["metal"]+score["wool"])                 #max 30 per level played
    attack = int(score["lumber"]+score["metal"])                                #max 20 per level played
    health = int(score["honey"]+score["berry"])                                 #max 100 per level played
    cAttack = int(score["metal"]+score["honey"]/5)                              #max 20 per level played

    me = bossPlayer(defense, attack, health, cAttack, "me", score["n"])
    boss = bossPlayer(defense, attack, health, cAttack, "boss", score["n"])

    meHealthBar = bossBox(410, 20, "healthbar")
    meHealthBarInside = bossBox(415, 25, "healthbarinside")
    bossHealthBar = bossBox(20, 20, "healthbar")
    bossHealthBarInside = bossBox(25, 25, "healthbarinside")
    meAttackBox = bossBox(20, 480, "attack")
    meDefenseBox = bossBox(580, 480, "defend")

    clock = pygame.time.Clock()
    kg = True
    start = int(time.time())

    yourTurn = True

    while kg:
        clock.tick(30)
        end = int(time.time())
        timePassed = int(end-start)

        boxes = [meHealthBar, meHealthBarInside, bossHealthBar, bossHealthBarInside, meAttackBox, meDefenseBox]
        bossBackground(background, boxes)

        if pygame.event.peek(QUIT) == True:                                     #checks for the event quit
            pygame.display.quit()
            pygame.mixer.music.stop()
            quit()

        if yourTurn == True:                                                    #if your turn is true
            printWord("YOUR TURN", (255,255,255), 0, 0, 100)
            for ev in pygame.event.get():                                       #checks for mouse being pressed
                if ev.type == MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if x >= 20 and x <= 220 and y >= 480 and y <= 580:          #the user chose attack
                        image = pygame.image.load("boss\\boss me attack.png")
                        screen.blit(image, (0,0))
                        bossPersonAttack(me, boss, bossHealthBarInside)
                        pygame.display.flip()
                        time.sleep(1)
                    elif x >= 580 and x <= 780 and y >= 480 and y <= 580:       #the user chose defense
                        image = pygame.image.load("boss\\boss me defend.png")
                        screen.blit(image, (0,0))
                        me.actionDefense()
                        printWord("You defended!", (255,255,255), 0, 500, 35)
                        pygame.display.flip()
                        time.sleep(1)
                    yourTurn = False
                    pygame.display.flip()
                    time.sleep(1)
                    bossBackground(background, boxes)
        else:                                                                   #if it's the boss's turn
            time.sleep(1)
            ba = bossAction()                                                   #the boss decides whether to attack or defend
            if ba == "a":                                                       #the boss decides to attack
                image = pygame.image.load("boss\\boss boss attack.png")
                screen.blit(image, (0,0))
                bossPersonAttack(boss, me, meHealthBarInside)
                pygame.display.flip()
                time.sleep(1)
            elif ba == "d":                                                     #the boss decides to defend
                image = pygame.image.load("boss\\boss boss defend.png")
                screen.blit(image, (0,0))
                boss.actionDefense()
                printWord("The boss defended!", (255,255,255), 0, 500, 35)
                pygame.display.flip()
                time.sleep(1)
            yourTurn = True
            pygame.display.flip()
            time.sleep(1)

        if me.health <= 0:                                                      #if your health is zero, the boss wins
            bossBackground(background, boxes)
            printWord("BOSS WINS!", (255,0,0), 0, 0, 100)
            pygame.display.flip()
            time.sleep(3)
            return False
        elif boss.health <= 0:                                                  #if the boss's health is zero, you win
            bossBackground(background, boxes)
            printWord("YOU WIN!", (255,255,255), 0, 0, 100)
            pygame.display.flip()
            time.sleep(3)
            return True

        pygame.display.flip()

def boss(score):                                                                #executes the entire game
    bossStart()
    win = bossGame(score)
    return win