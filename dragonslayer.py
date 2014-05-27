############################################
#                                          #
#  DDDD   RRR     A     GGG    OOO  N   N  #
#  D   D  R  R   A A   G   G  O   O N   N  #
#  D   D  R  R  A   A  G      O   O NN  N  #
#  D   D  RRR   AAAAA  G  GGG O   O N N N  #
#  DDDD   R  R  A   A   GGG G  OOO  N  NN  #
#                                          #
############################################
# coded by:         Kaylyn Garnett
# version:          0.0

# import libraries
#import random
from drawings import *
from libv0_0 import *
from text import *
import sys
import os
import copy


# size in terms of number of characters per line
gameWidth = 100
gameHeight = 40

# game settings
primaryBorder = ["@", "#", "*"]
secondaryBorder = ["o", "+", " "]
os.system("mode con cols=101 lines=41")
os.system('COLOR 0C')

# GAMEVARS
state = "reset"
mapDim = [4,4]

allEquipment = [eBroadsword, eSpikyHelm, eSpikyBoots, eChainmail, eBelt, eShield]

#creating the set of possible npcs/events to encounter
dictEventIndex = {
    'DRAGON':0,
    'BATS':1,
    'CAVEIN':2,
    'SKELETON':3
    }




# game loop
while state != "quit":

    #run through appropriate gamestate loop(s)
    while state == "intro":
        drawBasicOptionsScreen(gameWidth, gameHeight, primaryBorder, secondaryBorder, \
                               bufferColumn([dDragonSlayerLogo, pCredits]), pIntroText, pIntroOptions)
        userInput = input()
        state = checkUniversalOptions(userInput.lower(), state)
    #end intro loop
    
    while state == "play":
        #actions that are directly related to playing the game
        #seperated into smaller "gamestates" with if/else (ensure proper enter/exit for settings/quit options)
        #determined by coord relations

        #if player is not in same space as an npc/event, must choose route to take
        if (currentCoords not in eventCoords) or (currentCoords == eventCoords[dictEventIndex["SKELETON"]]):
            #update text to be shown to player
            availableRoutes = generateOptions(mapDim, currentCoords)
            screenMessage = eventLog + generateWarnings(mapDim, currentCoords, eventCoords)               
                
            
            #create drawing of tunnels to be shown (relative to options available)
            tunnels = []
            for i in range(0, len(availableRoutes)):
                tunnels.append(bufferColumn([dTunnel, stringToParagraph(availableRoutes[i], len(availableRoutes[i]))]))
            tunnelsImage = bufferRowWidth(tunnels, int(gameWidth*4/5))
            
            if (currentCoords == eventCoords[dictEventIndex["SKELETON"]]):
                #generate messages and generate an equip to find
                screenMessage.append(sSkeletonEncounter)
                newEquip = allEquipment[random.randint(0, len(allEquipment)-1)]
                screenMessage.append(sLootSkeleton + newEquip[1])
                #equip the item
                equipItem(playerInfo, newEquip)
                #update the screen image to show skeleton
                tunnelsImage = bufferColumn([tunnelsImage, dSkeleton])
                eventCoords[dictEventIndex["SKELETON"]] = generateRandomCoords(mapDim, [[currentCoords] + eventCoords])
            

            #draw everything to the screen
            drawBasicOptionsScreen(gameWidth, gameHeight, primaryBorder, secondaryBorder, tunnelsImage, screenMessage, pInCaveOptions)
            
            #get the users input
            userInput = input()
            #convert that to a state change
            if userInput.capitalize() in availableRoutes:
                eventLog = [sEnterRoom]
                moveTo(currentCoords, userInput.lower())
            elif userInput.capitalize() not in (pGenericOptions + pIntroOptions):
                eventLog = [sInvalidDirection]
            state = checkUniversalOptions(userInput.lower(), state)
            
                
        elif currentCoords == eventCoords[dictEventIndex["DRAGON"]]:
            #enter battle scene!
            battle = "true"
            eventLog = [sDragonEncounter]
            updatePlayerInfo(playerInfo)

            while battle == "true":
                battleImage = createBattleImage(gameWidth, dragonInfo, playerInfo)
                drawBattleScreen(gameWidth, gameHeight, primaryBorder, secondaryBorder, battleImage, eventLog, pInBattleOptions)
                #reset eventlog messages
                eventLog = [""]

                #deal with user interactions
                userInput = input()
                state = checkUniversalOptions(userInput.lower(), state)
                if userInput.lower() == "attack":
                    attack(playerInfo, dragonInfo, eventLog)
                    attack(dragonInfo, playerInfo, eventLog)
                    #deal with deaths
                    if playerInfo[2] >= playerInfo[3] and dragonInfo[2] >= dragonInfo[3]:
                        state = "gameOver"
                        gameOverImage = bufferColumn([[""], dGameOver])
                        gameOverMessage = sBothDead
                        battle = "false"
                    elif playerInfo[2] >= playerInfo[3]:
                        state = "gameOver"
                        gameOverImage = bufferColumn([dragonInfo[0], dGameOver])
                        gameOverMessage = sDeathByDragon
                        battle = "false"
                    elif dragonInfo[2] >= dragonInfo[3]:
                        state = "gameOver"
                        gameOverImage = bufferColumn([playerInfo[0], dCongrats])
                        gameOverMessage = [sDragonDead, sWinMessage]
                        battle = "false"
                    
                    
                elif userInput.lower() == "run":
                    eventLog.append(sRunFromDragon)
                    eventLog.append(sWellRested)
                    dragonInfo[2] = 0
                    playerInfo[2] = 0
                    currentCoords = generateRandomCoords(mapDim, [currentCoords] + eventCoords)  
                    battle = "false"
                

        elif currentCoords == eventCoords[dictEventIndex["BATS"]]:
            #what happens when you share spot with the tele-bats
            #show special bat even screen
            batSwarm = createTiledImage(gameWidth, gameHeight, dBat)
            drawBasicOptionsScreen(gameWidth, gameHeight, primaryBorder, secondaryBorder, batSwarm, [sBatEncounter], pBatOptions)

            #change coords once the user presses enter
            #get the users input
            userInput = input()
            #convert that to a state change
            if userInput == "":
                #teleport to a new and empty space
                currentCoords = generateRandomCoords(mapDim, [])
                while currentCoords in eventCoords:
                    currentCoords = generateRandomCoords(mapDim, [])
            state = checkUniversalOptions(userInput.lower(), state)

        elif currentCoords == eventCoords[dictEventIndex["CAVEIN"]]:
            #insta death if you encounter this
            killersMugShot = []
            for i in range(0, 4):
                num = random.randint(0,3)
                if num == 0:
                    killersMugShot.append(dTRock)
                elif num == 1:
                    killersMugShot.append(dSRock)
                elif num == 2:
                    killersMugShot.append(dMRock)
                elif num == 3:
                    killersMugShot.append(dLRock)
            killersMugShot = compressRowBottom(killersMugShot)
            gameOverMessage = sCaveIn
            gameOverImage = bufferColumn([killersMugShot, dGameOver])
            state = "gameOver"
            
            
    #end play loop

    while state == "gameOver":
        drawBasicOptionsScreen(gameWidth, gameHeight, primaryBorder, secondaryBorder, gameOverImage, gameOverMessage, pEndOptions)
        state = "reset"
        input()

    while state == "reset":
        #reset all the values
        #RESETABLE VALUES
        eventLog = [""]
        currentCoords = generateRandomCoords(mapDim, [[]])
        eventCoords = []
        eventCoords.append(generateRandomCoords(mapDim, [currentCoords]))
        for i in range(1, len(dictEventIndex)):
            #generate each events coords, ensuring they dont spawn on top of player
            eventCoords.append(generateRandomCoords(mapDim, [currentCoords] + eventCoords))

        playerInfo = copy.deepcopy(playerInfoDefault)
        playerInfo[0] = generateCharDrawing(playerInfo[6])
        dragonInfo = copy.deepcopy(dragonInfoDefault)

        state = "intro"


# end game loop

# draw a final game over screen before user exits
