import time
import random
import pygame
from pygame.locals import *
pygame.init()
pygame.mixer.init()

from lumberjack import *
from metalminer import *
from honeyhoarder import *
from berrilicious import *
from woolworld import *
from boss import *

wScreen, hScreen = 800, 600                                                     #this is the screen
screen = pygame.display.set_mode((wScreen, hScreen))
pygame.display.set_caption("Hamlet Hero by Anya & Fei")

musictype = ".wav"#".mp3"

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

def blitScreen(image, t, text, b):                                              #this blits each screen of the animation
    screen.blit(image, (0,0))
    if text != "":
        printWord(text, (255,255,255), 0, 500, 30)
    if b:
        button = pygame.image.load("replay\\next.png").convert()
        screen.blit(button, (590,10))
    pygame.display.flip()
    time.sleep(t)

def dialogueAnimation(texts):                                                   #input text and outputs a series of animation in the form of a dialogue
    imageMeAlone = pygame.image.load("intro\\intro me alone.png").convert()
    imageRegular = pygame.image.load("intro\\intro regular.png").convert()
    imageMe = pygame.image.load("intro\\intro me.png").convert()
    imageMayor = pygame.image.load("intro\\intro mayor.png").convert()

    blitScreen(imageMeAlone, 1, "", False)
    blitScreen(imageRegular, 1, "", False)

    index = 0
    kg = True
    while kg:
        if pygame.event.peek(QUIT) == True:
            pygame.display.quit()
            pygame.mixer.music.stop()
            quit()
        for ev in pygame.event.get():                                           #checks for left or right key
            if texts[index][0] == "mayor":
                blitScreen(imageMayor, 0, texts[index][1], True)
            elif texts[index][0] == "me":
                blitScreen(imageMe, 0, texts[index][1], True)
            if ev.type == MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if x > 590 and x < 790 and y > 10 and y < 110:
                    index += 1
                    if index >= len(texts):
                        return None

def introAnimation():                                                           #intro animation texts
    imageTitle = pygame.image.load("intro\\intro title.png").convert()
    blitScreen(imageTitle, 3, "", False)
    texts = [["mayor",   "Hello. My name is Mayor Gigi Greenwald."],
            ["mayor",   "If you know what's good for you, you'll get out of town."],
            ["me",      "???"],
            ["mayor",   "It is known that these part of the woods..."],
            ["mayor",   "...are ravaged by a fearsome monster."],
            ["mayor",   "Our hamlet has been suffering for far too long."],
            ["mayor",   "We do not wish this tragedy upon you, stranger."],
            ["me",      "!!!"],
            ["mayor",   "What do you mean?"],
            ["mayor",   "You can help?"],
            ["me",      ":)"],
            ["mayor",   "Oh thank you."],
            ["mayor",   "This hamlet is so lucky to have a hero like you."],
            ["me",      ":((("],
            ["mayor",   "Oh dear?"],
            ["mayor",   "You don't have any supplies?"],
            ["mayor",   "Fortunately we live in such a..."],
            ["mayor",   "...resourceful area in the woods."],
            ["mayor",   "I'm sure you can find something around here."],
            ["me",      ":)))"],
            ["mayor",   "And one more thing..."],
            ["mayor",   "Good luck."]]
    dialogueAnimation(texts)

def outroBadAnimation():                                                        #bad outro animation, played if the user loses
    texts = [["mayor",  "Oh no! The monster wasn't defeated?"],
            ["mayor",   "And it's coming to eat our children?"],
            ["me",      ":(("],
            ["mayor",   "You are no hero."],
            ["mayor",   "Let's wish the next town you visit..."],
            ["mayor",   "...has more fortune than ours."],
            ["mayor",   "Good day sir!"]]
    dialogueAnimation(texts)

def outroGoodAnimation():                                                       #good outro animation, played if the user wins
    texts = [["mayor",   "You did it! You got rid of the monster!"],
            ["mayor",   "Our hamlet thanks you so much for this great victory."],
            ["me",      ":)))"],
            ["mayor",   "For your bravery..."],
            ["mayor",   "...you can come to visit this town at any time."],
            ["me",      ":)"],
            ["mayor",   "Thank you stranger."],
            ["mayor",   "Thank you."]]
    dialogueAnimation(texts)

def miniGames(level, score):                                                    #plays the mini-games in a random order
    allGames = ["lumber", "metal", "wool", "honey", "berry"]
    random.shuffle(allGames)
    for g in allGames:
        time.sleep(5)
        pygame.mixer.music.load(g + "\\" + g + musictype)
        pygame.mixer.music.play()
        if g == "lumber":
            s = lumber(level)
        elif g == "metal":
            s = metal(level)
        elif g == "wool":
            s = wool(level)
        elif g == "honey":
            s = honey(level)
        elif g == "berry":
            s = berry(level)
        score[g] += s
        pygame.mixer.music.stop()
        pygame.display.set_caption("Hamlet Hero by Anya & Fei")
    score["n"] = level
    return score

def instruction():                                                              #shows the instructions of the game
    background = pygame.image.load("replay\\instruction.png").convert()
    button = pygame.image.load("replay\\next.png").convert()
    kg = True
    while kg:
        screen.blit(background, (0,0))
        screen.blit(button, (590,490))
        pygame.display.flip()
        if pygame.event.peek(QUIT) == True:                                     #checks for the event quit
            pygame.display.quit()
            pygame.mixer.music.stop()
            quit()
        for ev in pygame.event.get():                                           #checks for mouse keep down
            if ev.type == MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if 590 < x < 790 and 490 < y < 590:
                    return None

def replay(score):                                                              #shows the replay option
    background = pygame.image.load("replay\\replay background.png").convert()
    replayBox = pygame.image.load("replay\\replay replay.png").convert()
    bossBox = pygame.image.load("replay\\replay boss time.png").convert()

    stats = ["health: " + str(score["honey"]+score["berry"]),
            "attack: " + str(score["lumber"]+score["metal"]),
            "defense: " + str(score["lumber"]+score["metal"])]

    kg = True
    while kg:
        screen.blit(background, (0,0))
        screen.blit(replayBox, (70,20))
        screen.blit(bossBox, (70, 140))
        y2 = 300
        for s in stats:
            printWord(s, (255,255,255), 0, y2, 50)
            y2 += 100

        pygame.display.flip()

        if pygame.event.peek(QUIT) == True:
            pygame.display.quit()
            quit()
        for ev in pygame.event.get():
            if ev.type == MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if x >= 70 and x <= 370 and y >= 20 and y <= 120:               #if pressed replay, return True
                    return True
                elif x >= 70 and x <= 370 and y >= 140 and y <= 240:            #if pressed boss time, return False
                    return False

#OVERALL GAME
def game():                                                                     #executes the entire game
    pygame.mixer.music.load("intro\\intro%s"%musictype)
    pygame.mixer.music.play()
    introAnimation()                                                            #shows the intro music
    pygame.mixer.music.stop()

    instruction()

    level = 1
    score = {"n": 0, "lumber": 0, "metal": 0, "wool": 0, "honey": 0, "berry": 0}#set up scores

    r = True
    levels = 2
    for level in [1,2]:
        if r:                                                                   #if the user does not replay (after 1st round of mini-games), they will enter boss level
           score = miniGames(level, score)                                      #plays the mini-games
           if level < 2:
              r = replay(score)                                                 #show the replay option

    pygame.mixer.music.load("boss\\boss%s"%musictype)
    pygame.mixer.music.play()
    win = boss(score)                                                           #enters boss level
    pygame.mixer.music.stop()
    if win == True:                                                             #if user wins, then the good outro plays
        pygame.mixer.music.load("intro\\intro%s"%musictype)
        pygame.mixer.music.play()
        outroGoodAnimation()
    else:                                                                       #if user loses, then the bad outro plays
        pygame.mixer.music.load("outro\\outrobad%s"%musictype)
        pygame.mixer.music.play()
        outroBadAnimation()

game()
pygame.display.quit()
pygame.mixer.music.stop()
quit()
