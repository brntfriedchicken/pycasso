import pyautogui as py
import pygetwindow as gw
from math import floor
from random import randint, random
from PIL import Image

path = input("Drag image here then press ENTER: ")
img = Image.open(path)

canvasOffset = (5, 144)
editColors = (999, 89)
editColorsR = (1153, 593)
editColorsG = (1153, 616)
editColorsB = (1153, 638)
editColorsOK = (774, 658)

clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
maxStrokes = 3
strokeOffset = 20
strokeLengthOffset = 35
strokeCount = 0
color = []
x1 = 0
x2 = 0
y1 = 0
y2 = 0

def calibrate():
    global canvasOffset
    global editColors
    global editColorsR
    global editColorsG
    global editColorsB
    global editColorsOK

    input("Set the canvas dimensions to match the image dimensions then press ENTER")
    input("Move cursor over (0, 0) on canvas then press ENTER")
    canvasOffset = py.position()
    input("Move cursor over the Edit Colors button then press ENTER")
    editColors = py.position()
    input("move cursor over the R value in the Edit Colors panel then press ENTER")
    editColorsR = py.position()
    editColorsG = (py.position()[0], py.position()[1] + 20)
    editColorsB = (py.position()[0], py.position()[1] + 40)
    input("move cursor over the OK button in the Edit Colors panel then press ENTER")
    editColorsOK = py.position()
    input("The program has been calibrated")
    input("Press ENTER To Start")

def randRange(start, end):
    return floor(random() * (end - start) + start)

def draw(startX, startY, endX, endY):
    py.moveTo(canvasOffset[0] + startX, canvasOffset[1] + startY)
    py.dragTo(canvasOffset[0] + endX, canvasOffset[1] + endY)

def setColor(r, g, b):
    # Move over edit colors
    py.moveTo(editColors[0], editColors[1])
    py.click()
    # Set R value
    py.moveTo(editColorsR[0], editColorsR[1])
    py.click(clicks=2)
    py.typewrite(str(r))
    # Set G value
    py.moveTo(editColorsG[0], editColorsG[1])
    py.click(clicks=2)
    py.typewrite(str(g))
    # Set B value
    py.moveTo(editColorsB[0], editColorsB[1])
    py.click(clicks=2)
    py.typewrite(str(b))
    # Click OK
    py.moveTo(editColorsOK[0], editColorsOK[1])
    py.click()

def newStroke():
    global x1
    global y1
    global x2
    global y2
    global color

    color.clear()

    x1 = randint(0, img.size[0]-1)
    y1 = randint(0, img.size[1]-1)

    color.append(img.getpixel((x1, y1))[0])
    color.append(img.getpixel((x1, y1))[1])
    color.append(img.getpixel((x1, y1))[2])

    offsetLength = abs(random() * strokeLengthOffset)
    x2 = x1 + randRange(-offsetLength, offsetLength)
    y2 = y1 + randRange(-offsetLength, offsetLength)

mspaintWin = gw.getWindowsWithTitle('Paint')[0]

mspaintWin.maximize()

calibrate()
newStroke()
setColor(color[0], color[1], color[2])

while True:
        x1 += randRange(-strokeOffset, strokeOffset)
        y1 += randRange(-strokeOffset, strokeOffset)
        x2 += randRange(-strokeOffset, strokeOffset)
        y2 += randRange(-strokeOffset, strokeOffset)
        x1 = clamp(x1, 0, img.size[0]-1)
        y1 = clamp(y1, 0, img.size[1]-1)
        x2 = clamp(x2, 0, img.size[0]-1)
        y2 = clamp(y2, 0, img.size[1]-1)
        draw(x1, y1, x2, y2)

        strokeCount += 1
        if strokeCount % maxStrokes == 0:
            newStroke()
            setColor(color[0], color[1], color[2])