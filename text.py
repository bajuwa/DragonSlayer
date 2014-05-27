#  TEXT USED DURING GAME
# rules for options:  
# each option must be its own paragraph inside the set of options
from drawings import *


#equipment
#[0PIC, 1NAME, 2HPMOD, 3ATTMOD, 4DEFMOD, 5BODYPARTINDEX]
#bodypart index = 0feet, 1lefthand, 2belt, 3righthand, 4chest, 5head
eBareLeftHand = [dBareHand, "Bare Hand", 0, 1, 0, 1]
eBareRightHand = [dBareHand, "Bare Hand", 0, 1, 0, 3]
eBroadsword = [dBroadsword, "Broadsword", 0, 3, 0, 3]
eBald = [dBald, "Chrome Dome", 0, 0, 0, 5]
eSpikyHelm = [dSpikyHelm, "Spiky Helm", 1, 1, 1, 5]
eBareFeet = [dBareFeet, "Bare Feet", 0, 0, 0, 0]
eSpikyBoots = [dSpikyBoots, "Spiky Boots", 0, 1, 1, 0]
eBareChest = [dBareChest, "Bare Chest", 10, 0, 0, 4]
eChainmail = [dChainmail, "Chainmail", 15, 0, 1, 4]
eNoBelt = [dNoBelt, "Beltless", 0, 0, 0, 2]
eBelt = [dBelt, "Plain Belt", 2, 0, 0, 2]
eShield = [dShield, "Metal Shield", 0, 0, 3, 1]

#battle info
#[0BATTLEIMAGE, 1NAME, 2DAMAGETAKEN, 3MAXHEATLH, 4ATTACK, 5DEFENSE, 6[equipment]]
playerInfoDefault = [dStickman, "bajuwa", 0, 0, 0, 0, [eBareFeet, eBareLeftHand, eNoBelt, eBareRightHand, eBareChest, eBald]]
dragonInfoDefault = [dDragon, "Dragon", 0, 10, 5, 3, ['']]


pCredits = [
    "DragonSlayer",
    "v1.0",
    "",
    "Brought to you by:",
    "Kaylyn Garnett",
    "",
    "Text art from: patorjk.com/software/taag/"
    ]

pIntroText = ["Welcome to Dragon Slayer~!",
              "In this text-based dungeon crawler, you must traverse an intricate series of tunnels to find and slay the dragon!",
              "But it's not as simple as one may think, you'll need more than just your bare hands to slay the beast, and you'll need to find it all before the dragon finds you!"
              ]

pGenericOptions = [
    "Reset",
    "Quit"
    ]

pIntroOptions = [
    "Please type one of the following options: ",
    "Play"
    ]

pInCaveOptions = [
    "Please type a tunnel direction from above, or one of the following options: ",
    ""
    ]

pInBattleOptions = [
    "Please type one of the following options: ",
    "Attack",
    "Run"
    ]

pBatOptions = [
    "Press ENTER to figure out where you ended up...",
    ""
    ]

pEndOptions = [
    "Press ENTER to continue...",
    ""
    ]

sEnterRoom = "You emerge from the tunnel to find yourself in another cave..."
sInvalidDirection = "SMACK!  You walked face first into a solid wall.  Maybe you should pick one of the tunnels instead...."
sDragonWarning = "You hear the scratching of large claws from one of the tunnels..."
sBatWarning = "You hear a drone of frantic flapping coming from one of the tunnels..."
sCaveInWarning = "The walls around you seem cracked and unstable..."
sDeathByDragon = "The dragon roars in triumph as you fall to the floor, defeated by a mere beast..."
sBatEncounter = "You're enveloped by a swarm of flying bats as you enter the room!  Run away!!"
sCaveIn = "As soon as you step through the tunnel, the walls begin to crumble and fall, blocking your path.  You're screams are drowned out as the ceiling comes down on top of you, sealing you in your tomb."
sDragonEncounter = "Just as you enter the cave, the dragon stirs from atop its gold pile and begins to attack!"
sRunFromDragon = "Scared shitless, run through the tunnels, not knowing where you'll end up..."
sPlayerDead = "Your vision starts to blur and you begin you stagger.  You take one last look at your foe before you black out."
sDragonDead = "With a shriek of pain, the dragon lets loose its final roar and drops to the ground, dead at your feet."
sWinMessage = "You win.  Yay.  Figure out this message later."
sWellRested = "After a short rest, you feel refreshed and rejunivated."
sSkeletonEncounter = "You look down to see an armoured skeleton.  Looks like the dragon got the better of him."
sLootSkeleton = "You rummage through the bones and find a "
sSkeletonWarning = "Blood stains other signs of battle are riddled throughout the cave..."
