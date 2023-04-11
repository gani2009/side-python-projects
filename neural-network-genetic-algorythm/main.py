import numpy as np
import pygame
import math
import random
import json

pygame.init()

def toDegrees (angle):
    return angle * (180 / math.pi)

def toRadians (angle):
	return angle * (math.pi / 180)

def sinDegree(degrees):
	return round(math.sin(toRadians(degrees)) * 1000) / 1000

def cosDegree(degrees):
	return round(math.cos(toRadians(degrees)) * 1000 ) / 1000



class Layer:
    def __init__(this, n_inputs, n_neurons, weights=[]):
        if len(weights) == 0:
            this.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        else:
            this.weights = weights
        this.biases = np.zeros((1, n_neurons))
        this.inputs = n_inputs
        this.neurons = n_neurons
    def __str__(this):
        return f"Layer has {this.inputs} inputs and {this.neurons} neurons. "
    def resetWeights(this):
        this.weights = 0.10 * np.random.randn(this.inputs, this.neurons)
    def forward(this, inputs):
        this.output = np.dot(inputs, this.weights) + this.biases
    def returnWeightsBiases(this):
        return {"weights": this.weights, "biases": this.biases}


class Activation:
    def forward(this, inputs):
        this.output = np.maximum(0, inputs)


running = True
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Genetic Algorithm")
hugeText = pygame.font.SysFont(pygame.font.get_default_font(), 72)
largeText = pygame.font.SysFont(pygame.font.get_default_font(), 54)
bigText = pygame.font.SysFont(pygame.font.get_default_font(), 36)
mediumText = pygame.font.SysFont(pygame.font.get_default_font(), 24)
smallText = pygame.font.SysFont(pygame.font.get_default_font(), 18)

def addColors(color1, color2):
    redValue = round((color1[0]+color2[0])/2)
    greenValue = round((color1[1]+color2[1])/2)
    blueValue = round((color1[2]+color2[2])/2)
    return (redValue, greenValue, blueValue)

def collision(x1, y1, w1, h1, x2, y2, w2, h2):
    if x2 > w1 + x1 or x1 > w2 + x2 or y2 > h1 + y1 or y1 > h2 + y2:
        return False
    return True

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
violet = (255, 0, 255)
yellow = (255, 255, 0)
aqua = (0, 255, 255)
mode = 'menu'
halfway = math.sqrt(((screen.get_width()/2 - 0)*(screen.get_width()/2 - 0)) + ((screen.get_height()/2 - 0)*(screen.get_height()/2 - 0)))

def randomColor():
    return (round(random.random()*255), round(random.random()*255), round(random.random()*255))

def next():
    pass

creatures = []


class Creature:
    def __init__(this, color, network):
        this.color = color
        this.network = network
        this.x = round(random.random()*screen.get_width())
        this.y = round(random.random()*screen.get_height())
        this.width = 10
        this.xvel = 0
        this.yvel = 0
        this.max = 1
        this.senses = [0, 0, 0, 0]
        this.energy = 5
        this.age = 0
        this.randomNetwork()
    def __str__(this):
        return f"A {this.color} creature with a neural network with {len(this.network)+1} layers. The creature network has {this.network[0].inputs} inputs and {this.network[-1].neurons} outputs. Energy: {this.energy}"
    def networkForward(this):
        inputs = this.senses
        for layer in this.network:
            layer.forward(inputs)
            inputs = layer.output
        return inputs
    def randomNetwork(this):
        for layer in this.network:
            layer.resetWeights()
    def draw(this, simple=False):
        if simple:
            pygame.draw.rect(screen, this.color, pygame.Rect(this.x, this.y, this.width, this.width))
        else:
            this.senses = [this.x, this.y, screen.get_width() - this.x, screen.get_height() - this.y]
            this.x += this.xvel
            this.y += this.yvel
            networkOutput = this.networkForward()
            this.xvel += networkOutput[0][0]
            this.yvel += networkOutput[0][1]
            if abs(this.xvel) > this.max:
                this.xvel = this.max * (this.xvel / abs(this.xvel))
            if abs(this.yvel) > this.max:
                this.yvel = this.max * (this.yvel / abs(this.yvel))
            if this.x < 0:
                this.x = 0
            elif this.x + this.width > screen.get_width():
                this.x = screen.get_width() - this.width
            if this.y < 0:
                this.y = 0
            elif this.y + this.width > screen.get_height():
                this.y = screen.get_height() - this.width
            drawText(str(round(this.energy)), this.x, this.y+10, False, size=1)
            pygame.draw.rect(screen, this.color, pygame.Rect(this.x, this.y, this.width, this.width))


class Button:
    def __init__(this, x=100, y=100, w=100, h=100, c=(139, 139, 139), t="Button", onclick=next, border=True, center=False):
        this.x = x
        this.y = y
        this.initialx = x
        this.initialy = y
        this.w = w
        this.h = h
        this.c = c
        this.t = t
        this.o = onclick
        this.border = border
        this.center = center
    def draw(this):
        if this.center:
            this.x = this.x - this.w/2
            this.y = this.y - this.h/2
        pygame.draw.rect(screen, this.c, [this.x, this.y, this.w, this.h], 0)
        if this.border:
            pygame.draw.rect(screen, (0, 0, 0), [this.x-1, this.y-1, this.w+2, this.h+2], 1)
        text = bigText.render(this.t, True, (0, 0, 0))
        textX = this.x + ((this.w - text.get_width())/2)
        textY = this.y + ((this.h - text.get_height())/2)
        screen.blit(text, (textX, textY))
        this.x = this.initialx
        this.y = this.initialy
    def onclick(this, x, y):
        if this.x < x and this.y < y and this.x+this.w > x and this.y+this.h > y:
            this.o()


def drawText(text, x, y, center=True, color=(0,0,0), size=3):
    if size == 1:
        textT = smallText.render(text, True, color)
    elif size == 2:
        textT = mediumText.render(text, True, color)
    elif size == 3:
        textT = bigText.render(text, True, color)
    elif size == 4:
        textT = largeText.render(text, True, color)
    elif size == 5:
        textT = hugeText.render(text, True, color)
    
    if center:
        X = x - (textT.get_width() / 2)
    else:
        X = x
    screen.blit(textT, (X, y))

def stop():
    global running
    running = False
    for i in range(20):
        creatures.append(Creature(randomColor(), [Layer(4, 5), Layer(5, 3), Layer(3, 2)]))
start = Button(screen.get_width()/2-250, screen.get_height()/2-45, 500, 30, (255, 255, 255), "Start New", stop)
load = Button(screen.get_width()/2-250, screen.get_height()/2-45, 500, 30, (255, 255, 255), "Start New", stop)
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                mouseXY = pygame.mouse.get_pos()
                start.onclick(mouseXY[0], mouseXY[1])
    screen.fill("white")
    drawText("Genetic Algorithm", screen.get_width()/2, screen.get_height()/3, size=4)
    start.draw()
    # Render
    pygame.display.flip()

highScorer = {"score": 0}
energySource = Button(x=screen.get_width()/2, y=screen.get_height()/2, w=700, h=500, c=(255, 255, 255), t="Energy source", center=True)
running = True
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                mouseXY = pygame.mouse.get_pos()
            if mouse_presses[2] and mouse_presses[1]:
                mouseXY = pygame.mouse.get_pos()
                for creature in creatures:
                    creature.randomNetwork()
    screen.fill("white")
    energySource.w -= 0.0001
    energySource.h -= 0.0001
    energySource.draw()
    creatures.sort(key = lambda x: x.energy)
    if len(creatures) == 0:
        running = False
    elif creatures[0].energy > highScorer["score"]:
        highScorer = {"desc": str(creatures[0]), "score": creatures[0].energy, "creature": creatures[0]}
    # Render
    drawText(f"Population {len(creatures)}", screen.get_width()/2, 10)
    for creature in creatures[:]:
        creature.age -= 0.001
        if collision(creature.x, creature.y, creature.width, creature.width, energySource.x, energySource.y, energySource.w, energySource.h):
            creature.energy += 0.002
        creature.energy -= 0.001
        if creature.energy >= 15:
            network = creature.network
            for layer in network:
                layer.weights += 0.02 * np.random.randn(layer.inputs, layer.neurons)
            creatures.append(Creature(creature.color, network))
        elif creature.energy <= 0:
            creatures.remove(creature)
        if creature.age > 20:
            creatures.remove(creature)
        creature.draw()
    pygame.display.flip()


if highScorer["score"] > 0:
    print(highScorer['desc'])
    exitScene = True
    bestCreature = highScorer["creature"]
    bestCreature.width = 100
    bestCreature.x = 50
    bestCreature.y = 50
    while exitScene:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitScene = False
        screen.fill("white")
        # Render
        bestCreature.draw(True)
        drawText(str(bestCreature), screen.get_width()/2, 10, True, (0, 0, 0), 1)

        pygame.display.flip()
