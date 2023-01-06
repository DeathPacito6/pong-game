import os
import sys
import numpy as np
import math

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from GameComponents.Game import Game
from GameComponents.ControlledPaddle import ControlledPaddle

TARGET_TRAINING_DATAPOINTS = 50000
TARGET_TESTING_DATAPOINTS = 10000
TOTAL_DATAPOINTS = TARGET_TRAINING_DATAPOINTS + TARGET_TESTING_DATAPOINTS 

currentDatapoints = 0

trainingDataset = []
testingDataset = []

datasetNames = ["puckX", "puckY", "puckXspeed", "puckYspeed", "prediction"]


pygame.init()

surface = pygame.display.set_mode((650, 480))
icon = pygame.image.load(os.path.join("./", "icon.png"))

leftPaddle = ControlledPaddle(surface, True, True)
leftPaddle.brain.setJitter(True)
rightPaddle = ControlledPaddle(surface, True, False)
rightPaddle.brain.setJitter(True)

game = Game(surface, leftPaddle, rightPaddle, True)

leftPaddle.assignGame(game)
rightPaddle.assignGame(game)

def registerDatapoint():
    global currentDatapoints, trainingDataset, testingDataset
    if leftPaddle.brain.puckTrajectoryTowards:
        puckX = game.puck.left / game.screenWidth
        prediction = leftPaddle.brain.POI / game.screenHeight
    else:
        puckX = (game.screenWidth - game.puck.right) / game.screenWidth
        prediction = rightPaddle.brain.POI / game.screenHeight


    puckXspeed = abs(game.puck.speedX) / game.screenWidth
    puckY = game.puck.top / game.screenHeight
    puckYspeed = game.puck.speedY / game.screenWidth

    datapoint = (puckX, puckY, puckXspeed, puckYspeed, prediction)

    if currentDatapoints < TARGET_TRAINING_DATAPOINTS:
        if datapoint not in trainingDataset:
            trainingDataset.append(datapoint)
            currentDatapoints += 1
    elif currentDatapoints < TOTAL_DATAPOINTS:
        if datapoint not in trainingDataset or datapoint not in testingDataset:
            testingDataset.append(datapoint)
            currentDatapoints += 1
    
def updateProgressBar():
    barLen = 20
    percentComplete = currentDatapoints / TOTAL_DATAPOINTS
    numShown = math.floor(percentComplete * barLen)
    numHidden = barLen - numShown
    bar = f"[{'='*numShown}{' '*numHidden}]"

    print(f"\r{currentDatapoints}/{TOTAL_DATAPOINTS} - {bar} - {percentComplete * 100: .2f}%", end = " "*10)


while True:
    events = pygame.event.get()

    game.update(events)
    # game.render()
    pygame.display.flip()

    registerDatapoint()
    updateProgressBar()


    if currentDatapoints == TOTAL_DATAPOINTS:
        np.savetxt(f"./datasets/TRAIN{TARGET_TRAINING_DATAPOINTS}.csv", trainingDataset, delimiter=",")
        np.savetxt(f"./datasets/TEST{TARGET_TESTING_DATAPOINTS}.csv", testingDataset, delimiter=",")
        break


    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
    


