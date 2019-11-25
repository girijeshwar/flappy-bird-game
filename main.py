import random # for generating number
import sys # for exit the game/ programe
import pygame
from pygame.locals import *

#global variable for game 
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENHEIGHT, SCREENWIDTH))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = ''# ADDRESS
BACKGROUND = ''
PIPE = ''

def welcomeScreen():
    """
    shows welcome images on the screen
    """
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2
    messagex = int(SCREENWIDTH - GAME_SPRITES['message'].get_width())/2
    messagey = int(SCREENHEIGHT *0.13)
    basex= 0
    while True:
        for event in pygame.event.get():
            # if user click on cross key, closs the key
            if event.type == QUIT or(event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #if user presses spaces or up key, start the game for them
            elif event.type==KEYDOWN and (event.keys==K_SPACE or event.key ==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0 ))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery ))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey ))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playersx = int (SCREENWIDTH/5)                
    playery =int(SCREENWIDTH/2)
    basex= 0

    #create to pipe for blitting on screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #my list of upper pipe list of lower pipe
    upperPipes =[
        {'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]

    lowerPipes =[
        {'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]
    
    pipeVelX = -4

    playervelY = -9
    playerMaxvelY = -10
    playerMinvelY = -8
    playerAccY = 1

    playerFlapAccv = -8 #velocity while flapping
    playerFlapped = False # it is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type ==QUIT or (event.type ==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == k_UP):
                if playery >0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        #function wll return true if player is crashed
        if crashTest:
            return

        #check for score
        playerMidpos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            playerMidpos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width/2
            if pipeMidPos<= playerMidpos < pipeMidPos +4:
                score +=1
                print(f"your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVel, GROUNDY - playery - playerHeight)

        #move pipes to the left
        for upperPipe, lowerpipe in zip(upperPipes, lowerPipes):
             upperPipe['x'] += pipeVelX
             lowerpipe['x'] += pipeVelX

        #add anew pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

  


        #if pipe is out of the  screen, remove it
        if upperPipes[0]['x'] < - GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        for upperPipe, lowerpipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], lowerpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (upperPipe['x'], lowerpipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        
        myDigits = [int(x) for x in list(str(score))]
        width=0
        for digit in myDigits:
            width is GAME_SPRITES['numbers'][digits].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digits], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digits].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25 or playery<0:
        GAME_SOUNDS['hit'],play()
    return False


    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'],play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].getwidth):
            GAME_SOUNDS['hit'],play()
            return True

def getRandomPipe():
    """
    genrate posotion of two pipes(one bottom straight and one top rotated) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENWIDTH - GAME_SPRITES['base'].get_height - 1.2*offset))
    y1 = pipeHeight - y2 + offset
    pipe =[
        {'x': pipeX, 'y': y1},#upper pipe
        {'x': pipeX, 'y': y2}#lower pipe 
    ]
    return pipe
if __name__== "__main__":
   # this is where game being
   pygame.init()# initialize all pygame module
   FPSCLOCK = pygame.time.Clock()
   pygame.display.set_caption('Flappy bird by Girijeshwar singh')
   GAME_SPRITES['numbers'] = (
       pygame.image.load('Gallery/pic/0.png').convert_alpha(),
       pygame.image.load('Gallery/pic/1.png').convert_alpha(),
       pygame.image.load('Gallery/pic/2.png').convert_alpha(),
       pygame.image.load('Gallery/pic/3.png').convert_alpha(),
       pygame.image.load('Gallery/pic/4.png').convert_alpha(),
       pygame.image.load('Gallery/pic/5.png').convert_alpha(),
       pygame.image.load('Gallery/pic/6.png').convert_alpha(),
       pygame.image.load('Gallery/pic/7.png').convert_alpha(),
       pygame.image.load('Gallery/pic/8.png').convert_alpha(),
       pygame.image.load('Gallery/pic/9.png').convert_alpha(),
   )

   GAME_SPRITES['message'] = pygame.image.load('Gallery/pic/message.png').convert_alpha(),
   GAME_SPRITES['base'] = pygame.image.load('Gallery/pic/base.png').convert_alpha(),
   GAME_SPRITES['pipe'] = (
   pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
   pygame.image.load(PIPE).convert_alpha(),
   )
   #GAME SOUND
   GAME_SOUNDS['die'] = pygame.mixer.sound('Gallery/music/die.wav')
   GAME_SOUNDS['hit'] = pygame.mixer.sound('Gallery/music/hit.wav')
   GAME_SOUNDS['point'] = pygame.mixer.sound('Gallery/music/swoosh.wav')
   GAME_SOUNDS['swoosh'] = pygame.mixer.sound('Gallery/music/swoosh.wav')
   GAME_SOUNDS['wing'] = pygame.mixer.sound('Gallery/music/wing.wav')
     

   GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).conver()
   GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()



   while True:
       welcomeScreen() # shown welcome screem until user press any key
       mainGame
    