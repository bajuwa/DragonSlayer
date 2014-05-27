# library for dragonslayer game

import math
import random
from text import *
from drawings import *


# gameplay

#reminders:
#battle info: [0BATTLEIMAGE, 1NAME, 2DAMAGETAKEN, 3MAXHEATLH, 4ATTACK, 5DEFENSE, 6[equipment]]
#equipment: [0PIC, 1NAME, 2HPMOD, 3ATTMOD, 4DEFMOD]
def updatePlayerInfo(info):
    equips = info[6]
    info[0] = generateCharDrawing(equips)
    info[2] = 0
    info[3] = 0
    info[4] = 0
    info[5] = 0
    for i in range(0, len(equips)):
        temp = equips[i]
        info[3] += temp[2]
        info[4] += temp[3]
        info[5] += temp[4]

#equips an item to a player
def equipItem(player, equipment):
    currentEquips = player[6]
    currentEquips[equipment[5]] = equipment


#get the users input
def checkUniversalOptions(userInput, aState):
    #convert that to a state change
    if "play" in userInput.lower():
        return "play"
    elif "reset" in userInput.lower():
        return "reset"
    elif "quit" in userInput.lower():
        return "quit"
    else:
        return aState

# generates a random coordinate, but makes sure it isn't a certain given coord(s)
def generateRandomCoords(sizeOfMap, avoidCoords):
    coords = [random.randrange(0,sizeOfMap[0]), random.randrange(0,sizeOfMap[1])]
    while coords in avoidCoords:
        coords = [random.randrange(0,sizeOfMap[0]), random.randrange(0,sizeOfMap[1])]
    return coords

# generates the warnings applicable given the current coordinates, map size, and order-sensitive list of NPC coords
def generateWarnings(mapSize, coords, NPCcoords):
    warnings = []
    nCoords = generateNeighbourCoords(mapSize, coords)

    for i in range(0, len(nCoords)):
        if nCoords[i] == NPCcoords[0]: #DRAGONS
            warnings.append(sDragonWarning)
        if nCoords[i] == NPCcoords[1]: #BATS
            warnings.append(sBatWarning)
        if nCoords[i] == NPCcoords[2]: #CAVEIN
            warnings.append(sCaveInWarning)
        if nCoords[i] == NPCcoords[3]: #SKELETON
            warnings.append(sSkeletonWarning)

    return warnings

# generates the route options within the map dimension bounds
# doesn't give specifics, just gives n-e-s-w
def generateOptions(size, coords):
    options = []
    if (coords[1]+1) < size[1]:
        options.append("North")
    if (coords[0]+1) < size[0]:
        options.append("East")
    if (coords[1]-1) >= 0:
        options.append("South")
    if (coords[0]-1) >= 0:
        options.append("West")

    return options

# generates the route options within the map dimension bounds
# gives specific coordinates, used for inner calculations, not user-seen options
def generateNeighbourCoords(size, coords):
    neighbours = []
    if (coords[1]+1) < size[1]:
        neighbours.append([coords[0], coords[1]+1])
    if (coords[0]+1) < size[0]:
        neighbours.append([coords[0]+1, coords[1]])
    if (coords[1]-1) >= 0:
        neighbours.append([coords[0], coords[1]-1])
    if (coords[0]-1) >= 0:
        neighbours.append([coords[0]-1, coords[1]])

    return neighbours

#moves an entity to another coord based on n-e-s-w string directions
def moveTo(coords, strDirection):
    if strDirection.lower() == "north":
        coords[1] += 1
    if strDirection.lower() == "east":
        coords[0] += 1
    if strDirection.lower() == "south":
        coords[1] -= 1
    if strDirection.lower() == "west":
        coords[0] -= 1
    return coords



#determines how many instances of a single drawing can fit in a given area
def howManyCanFit(width, height, drawing):
    totalInRow = int(width/len(drawing[0]))
    totalInColumn = int(height/len(drawing))
    return (totalInRow * totalInColumn)

#determines if a row from a drawing is "empty" (either null space or all whitespace)
def isRowEmpty(string):
    if string == "":
        return "true"
    for i in range(0, len(string)):
        if string[i] != " ":
            return "false"
    return "true"


#takes stats from 2 entities, and calculates an attack from the first to the second, and updates with event messages
def attack(attacker, defender, events):
    #calculate damage
    attackValue = random.randint(0, attacker[4])
    defenceValue = random.randint(0, defender[5])
    damage = attackValue - defenceValue
    if damage < 0:
        damage = 0

    #deal damage and update eventLog
    defender[2] += damage
    events.append(str(attacker[1]) + " deals " + str(damage) + " damage to " + str(defender[1]) + "!")


# DISPLAY

# prints out a simple drawing
def draw(drawing):
    for i in range(0, len(drawing)):
        print(drawing[i])

# creates an image full with a repeated drawing
def createTiledImage(width, height, drawing):
    singleRow = bufferRow([drawing] * howManyCanFit(width, len(drawing), drawing))
    tiledImage = bufferColumn([singleRow] * howManyCanFit(len(singleRow[0]), height, singleRow))
    return tiledImage


#forms the image for displaying a 2way battle
def createBattleImage(width, leftEntity, rightEntity):
    leftImage = bufferDrawingBasic(createAttackerImage(leftEntity))
    rightImage = bufferDrawingBasic(createAttackerImage(rightEntity))
    return bufferRowBottomWidth([leftImage, rightImage], width)

def createAttackerImage(entity):
    healthBar = ["HP: " + "|"*(entity[3]-entity[2])]
    return bufferColumn([entity[0], stringToParagraph(entity[1], len(entity[1])), healthBar])

#generates a character image given the appropriate body parts
def generateCharDrawing(bodyParts):
    fullChar = dStickman[:]

    #make sure to keep the first 2 joint characters throughout attachment process
    for i in range(0, len(bodyParts)):
        tempEquip = bodyParts[i]
        fullChar = [fullChar[0]] + [fullChar[1]] + attachPieces(fullChar, tempEquip[0])

    return fullChar[2:]

#creates an image full of randomly placed drawings, higher the fullness -> higher number of drawings included, can exceed given dimensions
#doesn't really work =/
def createRandomizedDrawings(width, height, drawing):
    #going to keep adding images to each other until the determined width/height is obtained
    fullImage = drawing[:]
    while (len(fullImage) < height) or (len(fullImage[0]) < width):
        if len(fullImage) < height:
            #figure out max number of drawings that can fit in a new row, then choose a random number
            maxNumPerRow = howManyCanFit(len(fullImage[0]), len(drawing), drawing)
            newRow = bufferRowWidth([dBat*random.randint(math.ceil(maxNumPerRow/2), maxNumPerRow)], len(fullImage[0]))

            if random.randint(0, 1) == 0:
                fullImage = bufferColumn([fullImage, newRow])
            else:
                fullImage = bufferColumn([newRow, fullImage])

        if len(fullImage[0]) < width:
            #figure out max number of drawings that can fit in a new column, then choose a random number
            maxNumPerCol = howManyCanFit(len(drawing[0]), len(fullImage), drawing)
            newCol = bufferColumnHeight([dBat*random.randint(math.ceil(maxNumPerCol/2), maxNumPerCol)], len(fullImage[0]))

            if random.randint(0, 1) == 0:
                fullImage = bufferRow([fullImage, newCol])
            else:
                fullImage = bufferRow([newCol, fullImage])
    return fullImage





# draws a screen seperated into two fields, top = larger bordered image, bottom = smaller bordered image for messages/options
# note: options[0] must be the header to direct how to choose options
def drawBasicOptionsScreen(width, height, border1, border2, topImage, bottomMessage, options):
    wBorderWidth = width-4  # accounts for border space
    tempTopHeight = math.floor(height*2/3)  #accounts for screen divisions and border spaces
    tempBottomHeight = math.ceil(height/3)

    #creates the top screen
    topScreen = addBorder(bufferDrawingCenter(topImage, width, tempTopHeight), border1)

    #buffers the message and combines with options in specific format
    #space for options is always 3 (top = please choose..., middle = specific options, bottom = generic options)
    tempOptions = bufferWithGenericOptions(options[0], options[1:], wBorderWidth)
    message = bufferTextCenter(bottomMessage, wBorderWidth)
    message = bufferDrawingCenter(message, len(message[0]), len(message)+2) #creates extra space between messages n options
    messageWithOptions = bufferDrawingBasic(message + tempOptions)


    #creates the bottom screen
    bottomScreen = addBorder(bufferDrawingCenter(messageWithOptions, width, tempBottomHeight), border2)
    fullScreen = bufferColumn([topScreen, bottomScreen])

    draw(fullScreen)

def drawBattleScreen(width, height, border1, border2, topImage, bottomMessage, options):
    wBorderWidth = width-4  # accounts for border space
    tempTopHeight = math.floor(height*2/3)  #accounts for screen divisions and border spaces
    tempBottomHeight = math.ceil(height/3)

    #creates the top screen
    topScreen = addBorder(bufferDrawingCenter(topImage, width, tempTopHeight), border1)

    #buffers the message and combines with options in specific format
    #space for options is always 3 (top = please choose..., middle = specific options, bottom = generic options)
    tempOptions = bufferBasicOptions(options[0], options[1:], wBorderWidth)
    message = bufferTextCenter(bottomMessage, wBorderWidth)
    message = bufferDrawingCenter(message, len(message[0]), len(message)+2) #creates extra space between messages n options
    messageWithOptions = bufferDrawingBasic(message + tempOptions)


    #creates the bottom screen
    bottomScreen = addBorder(bufferDrawingCenter(messageWithOptions, width, tempBottomHeight), border2)
    fullScreen = bufferColumn([topScreen, bottomScreen])

    draw(fullScreen)

# takes a drawing and surrounds it with a border
# REPLACES what would normally be in the outside 2 characters where the border goes
# takes a LIST of characters for the border, ordered: corner, outside, inside
def addBorder(drawing, border):
    borderedDrawing = []
    height = len(drawing)
    width = len(drawing[0])
    # top of border
    borderedDrawing.append(str(border[0]) + str(border[1]) * (width-2) + str(border[0]))
    borderedDrawing.append(str(border[1]) + str(border[2]) * (width-2) + str(border[1]))

    # attaches the contents of the display
    for i in range(2, height-2):
        sampleLine = drawing[i]
        # attaches the appropriate line of the objects from top to bottom
        borderedDrawing.append(str(border[1]) + str(border[2]) + sampleLine[2:-2] + str(border[2]) + str(border[1]))

    # prints bottom of the border
    borderedDrawing.append(str(border[1]) + str(border[2]) * (width-2) + str(border[1]))
    borderedDrawing.append(str(border[0]) + str(border[1]) * (width-2) + str(border[0]))

    return borderedDrawing

#iterate through drawings and return the max height out of the drawings
def getMaxHeight(drawings):
    heightsOfDrawings = []
    for i in range(0, len(drawings)):
        heightsOfDrawings.append(len(drawings[i]))
    return max(heightsOfDrawings)

#iterate through drawings and return the max width out of the drawings
def getMaxWidth(drawings):
    widthsOfDrawings = []
    for i in range(0, len(drawings)):
        copyDrawing = bufferDrawingBasic(drawings[i])
        widthsOfDrawings.append(len(copyDrawing[0]))
    return max(widthsOfDrawings)

#takes a drawing, and adds whitespace to center the image in the proper dimensions
# removes any excess so that image is centered over-all
def bufferDrawingCenter(drawing, targetWidth, targetHeight):
    #create a new blank list to return as a modified drawing
    newDrawing = drawing[:]
    #if given an empty drawing, generate a blank drawing
    if len(newDrawing) == 0:
        for i in range(0, targetHeight):
            newDrawing.append(" " * targetWidth)
    else:
        # fix height
        while len(newDrawing) < targetHeight:
            newDrawing.insert(0, "")
            if len(newDrawing) < targetHeight:
                newDrawing.append("")
        if len(newDrawing) > targetHeight:
            topClipping = math.floor((len(newDrawing)-targetHeight)/2)
            bottomClipping = math.ceil((len(newDrawing)-targetHeight)/2)
            newDrawing = newDrawing[topClipping:-bottomClipping]

        # fix width
        for i in range(0, len(newDrawing)):
            if len(newDrawing[i]) < targetWidth:
                newDrawing[i] = (" " * math.floor((targetWidth-len(newDrawing[i]))/2)) \
                                + newDrawing[i] \
                                + (" " * math.ceil((targetWidth-len(newDrawing[i]))/2))
            else:
                sample = newDrawing[i]
                clipping = int((len(sample)-targetWidth)/2)
                newDrawing[i] = sample[clipping:len(sample)-clipping]

    return newDrawing

#takes a drawing, and adds whitespace to center the image in the smallest dimensions possible without cutting the image
def bufferDrawingBasic(drawing):
    #find the target widths and height for minimal whitespace
    height = len(drawing)

    #generate a list of all widths, then pick the max width
    widthList = []
    for i in range(0, len(drawing)):
        widthList.append(len(drawing[i]))
    width = max(widthList)

    #pass new arguments into proper buffering function and return picture
    return bufferDrawingCenter(drawing, width, height)

#takes drawing and buffers it, aligning the image to the LEFT of the given width
#   if drawing is wider than given width, right side of image will be cut off
#   for height, buffer to appropriate height/alignment seperately
def bufferDrawingLeft(drawing, width):
    copy = drawing[:]
    for i in range(0, len(copy)):
        if len(copy[i]) < width:
            copy[i] += " " * (width - len(copy[i]))
        else:
            sample = copy[i]
            copy[i] = sample[:width]
    return copy

#buffers drawing and aligns to the RIGHT of the given width
def bufferDrawingRight(drawing, width):
    copy = drawing[:]
    for i in range(0, len(copy)):
        if len(copy[i]) < width:
            copy[i] = " " * (width - len(copy[i])) + copy[i]
        else:
            sample = copy[i]
            copy[i] = sample[len(sample)-width:]
    return copy

#buffer an image, but aligns it to settle on the bottom of given dimensions
def bufferDrawingBottom(drawing, height):
    copy = bufferDrawingBasic(drawing)
    if len(copy) < height:
        copy = [" "*len(copy[0])] * (height-len(copy)) + copy
    return copy

#buffer an image, but aligns it to settle on the top of given dimensions
def bufferDrawingTop(drawing, height):
    copy = bufferDrawingBasic(drawing)
    if len(copy) < height:
        copy += [" "*len(copy[0])] * (height-len(copy))
    return copy


#same things as bufferDrawingLeft, except will only add as much whitespace as necessary
def bufferDrawingBasicLeft(drawing):
    widths = []
    for i in range(0, len(drawing)):
        widths.append(len(drawing[i]))
    maxWidth = max(widths)
    return bufferDrawingLeft(drawing, maxWidth)

# takes a list of drawings and combines them horizontally into a single drawing
def bufferRow(drawings):
    bufferedDrawings = bufferToSameHeight(drawings)
    return combineRow(bufferedDrawings)


# takes a list of drawings and combines them horizontally into a single drawing,  each image aligned to the bottom
def bufferRowBottom(drawings):
    bufferedDrawings = bufferToSameHeightBottom(drawings)
    return combineRow(bufferedDrawings)


# takes a list of drawings and combines them horizontally into a single drawing,  each image aligned to the top
def bufferRowTop(drawings):
    bufferedDrawings = bufferToSameHeightTop(drawings)
    return combineRow(bufferedDrawings)


# buffers row to a specific width, each imaged spaced evenly
def bufferRowWidth(drawings, width):
    #determine width of each individual drawings
    individualWidths = int(width/len(drawings))

    #buffer each drawing to desired width, don't change heights
    bufferedImages = []
    for i in range(0, len(drawings)):
        bufferedImages.append(bufferDrawingCenter(drawings[i], individualWidths, len(drawings[i])))

    #buffer them into a single image
    return bufferRow(bufferedImages)

# buffers row, but aligns each image to the bottom.
def bufferRowBottomWidth(drawings, width):
    bufferedImages = bufferToSameHeightBottom(drawings)
    return bufferRowWidth(bufferedImages, width)

# takes a list of drawings and combines them vertically into a single drawing from top to bottom
def bufferColumn(drawings):

    #get the width of each buffered drawing as a list
    widthOfDrawings = []
    for i in range(0, len(drawings)):
        sampleDrawing = bufferDrawingBasic(drawings[i])
        widthOfDrawings.append(len(sampleDrawing[0]))

    #buffer each image to the same width and combine
    bufferedDrawing = []
    for j in range(0, len(drawings)):
        bufferedDrawing += bufferDrawingCenter(drawings[j], max(widthOfDrawings), len(drawings[j]))

    return bufferedDrawing

#buffers to a specific height
def bufferColumnHeight(drawings, height):
    #determine height of each individual drawings
    individualHeights = int(height/len(drawings))

    #buffer each drawing to desired width, don't change heights
    bufferedImages = []
    for i in range(0, len(drawings)):
        sample = drawings[i]
        bufferedImages.append(bufferDrawingCenter(drawings[i], len(sample[0]), individualHeights))

    #buffer them into a single image
    return bufferColumn(bufferedImages)

#takes a set of drawings, returns them in a list, with all buffered to same height
def bufferToSameHeight(drawings):

    maxHeight = getMaxHeight(drawings)

    #buffer each image to the same height
    bufferedDrawings = drawings[:]
    for j in range(0, len(bufferedDrawings)):
        tempDrawing = bufferedDrawings[j] # used to get the width of the image
        bufferedDrawings[j] = bufferDrawingCenter(bufferedDrawings[j], len(tempDrawing[0]), maxHeight)

    return bufferedDrawings

#takes a set of drawings, returns them in a list, with all buffered to same height aligned at the bottom
def bufferToSameHeightBottom(drawings):

    maxHeight = getMaxHeight(drawings)

    #buffer each image to the same height
    bufferedDrawings = drawings[:]
    for j in range(0, len(drawings)):
        tempDrawing = drawings[j] # used to get the width of the image
        bufferedDrawings[j] = bufferDrawingBottom(bufferedDrawings[j], maxHeight)

    return bufferedDrawings

#takes drawings and buffers them to be the same width, returns a list of drawings
def bufferToSameWidth(drawings):

    maxWidth = getMaxWidth(drawings)

    #buffer each image to the same height
    bufferedDrawings = drawings[:]
    for j in range(0, len(bufferedDrawings)):
        bufferedDrawings[j] = bufferDrawingCenter(bufferedDrawings[j], maxWidth, len(bufferedDrawings[j]))

    return bufferedDrawings


#returns the number of instances of a certain char are found in a row, starting from the right
def numOfCharsFromRight(string, char):
    count = 0
    pointer = len(string)-1

    while string[pointer] == char:
        count += 1
        pointer -= 1
        if pointer == -1:
            return count

    return count

#returns the number of instances of a certain char are found in a row, starting from the left
def numOfCharsFromLeft(string, char):
    count = 0
    pointer = 0

    while string[pointer] == char:
        count += 1
        pointer += 1
        if pointer == len(string):
            return count

    return count

#returns the number of instances of a certain char are found in a column of a drawing, starting from the bottom
def numOfCharsFromBottom(drawing, column, char):
    count = 0
    pointer = len(drawing)-1
    tempRow = drawing[pointer]
    while tempRow[column] == char: #iterate through rows, bottom to top, if char is right
        count += 1
        pointer -= 1
        if pointer < 0:
            return count
        tempRow = drawing[pointer]

    return count

#returns the number of instances of a certain char are found in a column of a drawing, starting from the top
def numOfCharsFromTop(drawing, column, char):
    count = 0
    pointer = 0
    tempRow = drawing[pointer]
    while tempRow[column] == char: #iterate through rows, bottom to top, if char is right
        count += 1
        pointer += 1
        tempRow = drawing[pointer]

    return count

#combines images side by side without regards to buffering
def combineRow(drawings):
    fullDrawing = drawings[0]  #takes the first image, and modifies it by extending the strings/rows with that of other drawings
    for k in range(0, len(fullDrawing)):
        for l in range(1, len(drawings)):
            sampleDrawing = drawings[l]
            fullDrawing[k] += sampleDrawing[k]
    return fullDrawing

#takes 2 drawings, compresses them side by side while removing excess whitespace between drawings
def compressHorizontally(left, right):
    #create copy/base for the upcoming edits
    bufferedDrawings = bufferToSameHeight([left, right])
    tempLeft = bufferedDrawings[0]
    tempRight = bufferedDrawings[1]

    #use to store the amount of whitespace that's allowed to be removed
    excessWhitespace = len(tempLeft[0]) + len(tempRight[0]) #sets excess whitespace to max possible length

    #find out how much whitespace to trim out from between images
    for i in range(0, len(tempLeft)):
        totalLinesWS = numOfCharsFromRight(tempLeft[i], " ") + numOfCharsFromLeft(tempRight[i], " ")
        if totalLinesWS < excessWhitespace:
                excessWhitespace = totalLinesWS

    #now remove the excess whitespace from each image
    compressed = []
    for i in range(0, len(tempLeft)):  #iterate through each row of the drawing, from top to bottom
        tempValue = 0
        leftLine = tempLeft[i]
        rightLine = tempRight[i]
        while (tempValue < excessWhitespace) and (leftLine[-1] == " "):
            #first remove as much as possible from left drawing
            leftLine = leftLine[:-1]
            tempValue += 1
        #if more still needs to be removed, take it from right drawing
        while (tempValue < excessWhitespace) and (rightLine[0] == " "):
            rightLine = rightLine[1:]
            tempValue += 1
        #then add each line to the new drawing
        compressed.append(leftLine + rightLine)

    return compressed

#takes a set of drawings, combines them into a row while deleting excess whitespace between drawings
def compressRow(drawings):

    bufferedDrawings = bufferToSameHeight(drawings)

    while len(bufferedDrawings) > 2:
        bufferedDrawings = [compressHorizontally(bufferedDrawings[0], bufferedDrawings[1])] + bufferedDrawings[2:]
    if len(bufferedDrawings) == 2:
        bufferedDrawings = compressHorizontally(bufferedDrawings[0], bufferedDrawings[1])

    return bufferedDrawings

#compress drawings wtih specific alignment
def compressRowBottom(drawings):
    bufferedDrawings = bufferToSameHeightBottom(drawings)
    return compressRow(bufferedDrawings)

#takes 2 drawings, compresses them on top of eachother while removing excess whitespace between drawings
def compressVertically(top, bottom):
    #create copy/base for the upcoming edits
    tempTop = bufferDrawingCenter(top, max(len(top[0]), len(bottom[0])), max(len(top), len(bottom)))
    tempBottom = bufferDrawingCenter(bottom, max(len(top[0]), len(bottom[0])), max(len(top), len(bottom)))

    #use to store the amount of whitespace that's allowed to be removed
    excessWhitespace = len(tempTop) + len(tempBottom) #sets excess whitespace to max possible length

    #find out how much whitespace to trim out from between images
    for i in range(0, len(tempTop[0])): #iterate over columns
        totalColumnsWS = numOfCharsFromBottom(tempTop, i, " ") + numOfCharsFromTop(tempBottom, i, " ")
        if totalColumnsWS < excessWhitespace:
                excessWhitespace = totalColumnsWS

    #now remove the excess whitespace from each image by overlaying the bottom image over the top
    overlappedRows = overlayDrawings(tempTop[-excessWhitespace:], tempBottom[:excessWhitespace], " ")
    compressed = []
    compressed.extend(tempTop[:-excessWhitespace])
    compressed.extend(overlappedRows)
    compressed.extend(tempBottom[excessWhitespace:])

    return compressed

#takes a series of images and compresses them on top of eachother, eliminating excess whitespace between images, and stackes them from bottom up
def compressColumn(drawings):

    bufferedDrawings = bufferToSameWidth(drawings)

    while len(bufferedDrawings) > 2:
        bufferedDrawings = bufferedDrawings[:-2] + [compressVertically(bufferedDrawings[-2], bufferedDrawings[-1])]
    if len(bufferedDrawings) == 2:
        bufferedDrawings = compressVertically(bufferedDrawings[-2], bufferedDrawings[-1])

    return bufferedDrawings


#takes 2 drawings, and replaces the spaces on the first image, with data from the second image, skipping any CHARs in the overlaying drawing
def overlayDrawings(base, overlay, char):
    #make sure they are the same size
    copies = bufferToSameHeight([base, overlay])
    copies = bufferToSameWidth([copies[0], copies[1]])
    baseCopy = copies[0]
    overlayCopy = copies[1]
    fullDrawing = baseCopy[:]

    for i in range(0, len(baseCopy)): #iterate over rows
        tempBaseRow = baseCopy[i]
        tempOverlayRow = overlayCopy[i]
        for j in range(0, len(tempBaseRow)): #iterate over columns
            # use numOfChars to ensure that even intended spaces in the middle of a drawing get copied over
            if (j >= numOfCharsFromLeft(tempOverlayRow, char)) and (j < (len(tempOverlayRow) - numOfCharsFromRight(tempOverlayRow, char))):
                tempBaseRow = tempBaseRow[:j] + tempOverlayRow[j] + tempBaseRow[j+1:]
        fullDrawing[i] = tempBaseRow
    return fullDrawing

#takes two pieces that were created as 'puzzle piece' and sticks them together
#note: the first line of a 'puzzle piece' type drawing is a single char, this is where the joint between images will be
#note: the second line of a pp drawing is a single char, denoting what the joint-char should be replaced with ("", " ", "/", etcc)
#the first piece will be considered the base, and the second will be laid overtop
def attachPieces(basePiece, overlayPiece):
    #prep both pieces
    overlayJoint = overlayPiece[0]
    overlayMend = overlayPiece[1]
    overlay = bufferDrawingBasic(overlayPiece[2:])
    baseJoint = basePiece[0]
    baseMend = basePiece[1]
    base = basePiece[2:]
    base = bufferDrawingCenter(base, getMaxWidth([base])+(2*len(overlay[0])), getMaxHeight([base])+(2*len(overlay)))

    #find joints
    #find overlays joint and record it for later
    overlaysJointCoord = [0,0]
    for i in range(0, len(overlay)):
        tempRow = overlay[i]
        for j in range(0, len(tempRow)):
            if tempRow[j] == overlayJoint:
                overlaysJointCoord = [j, i]
                #mend the overlays joint, but don't do it to base (base may have multiple joint spots)
                overlay[i] = tempRow.replace(overlayJoint, overlayMend, 1)

    #find bases joint and record it for later
    basesJointCoord = [0,0]
    for i in range(0, len(base)):
        tempRow = base[i]
        for j in range(0, len(tempRow)):
            if tempRow[j] == baseJoint:
                basesJointCoord = [j, i]

    #overlay the two pieces
    #must buffer the overlay so that it's joint is in the same column as the bases, without regard to overall width
    #  math:   length of original overlay + difference of the 2 column index * 2 <- x2 because it must add the difference to both side of the drawing
    bufferedOverlay = bufferDrawingCenter(overlay, len(overlay[0])+(basesJointCoord[0]-overlaysJointCoord[0])*2, len(overlay))
    # then buffer to base's width to remove excess on the overlays right side
    bufferedOverlay = bufferDrawingLeft(bufferedOverlay, len(base[0]))

    #now find the area of the base that will need to be overlayed
    spliceRange = [basesJointCoord[1]-overlaysJointCoord[1], basesJointCoord[1]+len(overlay)-overlaysJointCoord[1]]
    baseSplice = base[spliceRange[0]:spliceRange[1]]
    overlayedSplice = overlayDrawings(baseSplice, bufferedOverlay, " ")

    #put the now combined rows back into their proper place in the base
    fullDrawing = base[:spliceRange[0]] + overlayedSplice + base[spliceRange[1]:]

    #trim all excess whitespace before returning final product
    return trimDrawing(fullDrawing)


#takes a single drawing, and trims it so that no excess whitespace lies outside the drawings
def trimDrawing(drawing):
    trimmed = drawing[:]
    #trim tops and bottoms of empty rows
    while isRowEmpty(trimmed[0]) == "true":
        trimmed = trimmed[1:]
    while isRowEmpty(trimmed[-1]) == "true":
        trimmed = trimmed[:-1]

    #then trim sides
    emptyRightSpace = []
    emptyLeftSpace = []
    for i in range(0, len(trimmed)):
        emptyRightSpace.append(numOfCharsFromRight(trimmed[i], " "))
        emptyLeftSpace.append(numOfCharsFromLeft(trimmed[i], " "))
    trimmed = bufferDrawingLeft(trimmed, len(trimmed[0])-min(emptyRightSpace))
    trimmed = bufferDrawingRight(trimmed, len(trimmed[0])-min(emptyLeftSpace))

    return trimmed


# takes a list of strings, with each string being a seperate paragraph, and formats them into a single drawing of text
# doesn't have a set height (it will be as long as it needs to be in order to fit all paragraphs)
def bufferTextCenter(paragraphs, targetWidth):
    fullText = []

    #if it's more than just a single string/paragraph, iterates through all paragraphs
    if isinstance(paragraphs, list):
        for i in range(0, len(paragraphs)):
            fullText.extend(stringToParagraph(paragraphs[i], targetWidth))
    #if it's just a single paragraph/string
    if isinstance(paragraphs, str):
        fullText.extend(stringToParagraph(paragraphs, targetWidth))
    #buffers the entire thing
    fullText = bufferDrawingCenter(fullText, targetWidth, len(fullText))

    return fullText

# takes a single string and converts it to a paragraph styled 'drawing'
def stringToParagraph(text, targetWidth):
    paragraph = []
    indexTracker = 0
    offset = 0

    #provided the text is wider than the target width, start at targetWidth index, the decrement til a space is found
    while (len(text)-indexTracker) > targetWidth:
        offset = 0
        while text[indexTracker+targetWidth-offset] != ' ':
            offset += 1
        paragraph.append(text[indexTracker:indexTracker+targetWidth-offset])
        indexTracker += targetWidth-offset
    # take the left over bit and add it
    paragraph.append(text[indexTracker:indexTracker+targetWidth-offset])

    return paragraph

# takes a list of options and formats them into a header, basic options, always followed by the generic options
def bufferWithGenericOptions(header, options, targetWidth):
    #show given header
    bufferedOptions = stringToParagraph(header, targetWidth)

    #show given options
    bufferedOptions += [""]  #append an empty line so that you can modify the string into the set of options on that line
    for i in range(0, len(options)):
        #creates options list that is centered into the middle part of the given width
        isample = bufferTextCenter(options[i], math.floor(targetWidth/(len(options)+2)))
        bufferedOptions[len(bufferedOptions)-1] += isample[0] # must do this as buffer returns a drawing (list of strings)

    #show the generic options
    bufferedOptions += [""]  #append an empty line so that you can modify the string into the set of options on that line
    for j in range(0, len(pGenericOptions)):
        #creates options list that is centered into the middle half of the given width
        jsample = bufferTextCenter(pGenericOptions[j], math.floor(targetWidth/(len(pGenericOptions)+2)))
        bufferedOptions[len(bufferedOptions)-1] += jsample[0] # must do this as buffer returns a drawing (list of strings)

    #buffer the final product
    return bufferDrawingBasic(bufferedOptions)

def bufferBasicOptions(header, options, targetWidth):
    #show given header
    bufferedOptions = stringToParagraph(header, targetWidth)

    #show given options
    bufferedOptions += [""]  #append an empty line so that you can modify the string into the set of options on that line
    for i in range(0, len(options)):
        #creates options list that is centered into the middle part of the given width
        isample = bufferTextCenter(options[i], math.floor(targetWidth/(len(options)+2)))
        bufferedOptions[len(bufferedOptions)-1] += isample[0] # must do this as buffer returns a drawing (list of strings)


    #buffer the final product
    return bufferDrawingBasic(bufferedOptions)
