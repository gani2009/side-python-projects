import numpy as np
import pygame
import math
import random
import copy
import datetime
import os
import sys
# from win11toast import toast
year = 1
startNum = 1000
forever = True
pygame.init()


def toDegrees(angle):
  return angle * (180 / math.pi)


def toRadians(angle):
  return angle * (math.pi / 180)


def sinDegree(degrees):
  return round(math.sin(toRadians(degrees)) * 1000) / 1000


def cosDegree(degrees):
  return round(math.cos(toRadians(degrees)) * 1000) / 1000


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
moniter = pygame.display.Info()
screen = pygame.display.set_mode((moniter.current_w-50, moniter.current_h-200))
pygame.display.set_caption("Genetic Algorithm")
hugeText = pygame.font.SysFont(pygame.font.get_default_font(), 72)
largeText = pygame.font.SysFont(pygame.font.get_default_font(), 54)
bigText = pygame.font.SysFont(pygame.font.get_default_font(), 36)
mediumText = pygame.font.SysFont(pygame.font.get_default_font(), 24)
smallText = pygame.font.SysFont(pygame.font.get_default_font(), 18)


def addColors(color1, color2):
  redValue = round((color1[0] + color2[0]) / 2)
  greenValue = round((color1[1] + color2[1]) / 2)
  blueValue = round((color1[2] + color2[2]) / 2)
  return (redValue, greenValue, blueValue)


def collision(x1, y1, w1, h1, x2, y2, w2, h2):
  if x2 > w1 + x1 or x1 > w2 + x2 or y2 > h1 + y1 or y1 > h2 + y2:
    return False
  else:
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
halfway = math.sqrt(((screen.get_width() / 2 - 0) *
                     (screen.get_width() / 2 - 0)) +
                    ((screen.get_height() / 2 - 0) *
                     (screen.get_height() / 2 - 0)))


def randomColor():
  return (round(random.random() * 255), round(random.random() * 255),
          round(random.random() * 255))


def next():
  pass


creatures = []


class Button:

  def __init__(this,
               x=100,
               y=100,
               w=100,
               h=100,
               c=(139, 139, 139),
               t="Button",
               onclick=next,
               border=True,
               center=False):
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
    this.rect = [this.x, this.y, this.w, this.h]

  def draw(this):
    if this.center:
      this.x = this.x - this.w / 2
      this.y = this.y - this.h / 2
      this.rect = [this.x, this.y, this.w, this.h]
    pygame.draw.rect(screen, this.c, [this.x, this.y, this.w, this.h], 0)
    if this.border:
      pygame.draw.rect(screen, (0, 0, 0),
                       [this.x - 1, this.y - 1, this.w + 2, this.h + 2], 1)
    text = bigText.render(this.t, True, (0, 0, 0))
    textX = this.x + ((this.w - text.get_width()) / 2)
    textY = this.y + ((this.h - text.get_height()) / 2)
    screen.blit(text, (textX, textY))
    this.x = this.initialx
    this.y = this.initialy

  def onclick(this, x, y):
    if this.x < x and this.y < y and this.x + this.w > x and this.y + this.h > y:
      this.o()


energySource = Button(x=screen.get_width() / 2,
                      y=screen.get_height() / 2,
                      w=screen.get_width()/1.5,
                      h=screen.get_height()/1.5,
                      c=(255, 255, 255),
                      t="Energy source",
                      center=True)

class Creature:

  def __init__(this, color, network):
    this.color = color
    this.network = network
    this.x = round(random.random() * screen.get_width())
    this.y = round(random.random() * screen.get_height())
    this.width = 10
    this.xvel = 0
    this.yvel = 0
    this.max = 1
    this.senses = [0, 0, 0, 0]
    this.energy = 5
    this.age = 0
    this.energyConsumption = 0.006
    this.energyUsage = 0.001
    this.randomNetwork()

  def __str__(this):
    return f"A {this.color} cell. Neural network has {len(this.network)+1} layers, {this.network[0].inputs} inputs and {this.network[-1].neurons} outputs. Energy: {round(this.energy)}(Usage: {round(this.energyUsage)};Consumption: {round(this.energyConsumption)}). Age: {round(this.age)}. Current year: {round(year)}"

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
      pygame.draw.rect(screen, this.color,
                       pygame.Rect(this.x, this.y, this.width, this.width))
    else:
      if this.age > 20:
        this.width = this.age/2
        this.energyConsumption = this.age/2 * 0.0006
        this.energyUsage = this.age/2 * 0.0001
      this.senses = [
        this.x, this.y,
        energySource.x, energySource.y
      ]
      this.x += this.xvel
      this.y += this.yvel
      networkOutput = this.networkForward()
      this.xvel += networkOutput[0][0]*2
      this.yvel += networkOutput[0][1]*2
      if abs(this.xvel) > this.max:
        this.xvel = this.max * (this.xvel / abs(this.xvel))
      if abs(this.yvel) > this.max:
        this.yvel = this.max * (this.yvel / abs(this.yvel))
      pygame.draw.rect(screen, this.color,
                       pygame.Rect(this.x, this.y, this.width, this.width))


def drawText(text, x, y, center=True, color=(0, 0, 0), size=3):
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

start = Button(screen.get_width() / 2,
               screen.get_height() / 2, 500, 30, (255, 255, 255),
               "Start New", stop, center=True)
while running and forever == False:
  screen.fill("white")
  drawText("Genetic Algorithm",
           screen.get_width() / 2,
           screen.get_height() / 3,
           size=4)
  start.draw()
  # Render
  # Events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_presses = pygame.mouse.get_pressed()
      if mouse_presses[0]:
        mouseXY = pygame.mouse.get_pos()
        start.onclick(mouseXY[0], mouseXY[1])
  pygame.display.flip()

highScorer = {"score": 0}
screen.fill("white")
drawText("Loading...", screen.get_width()/2, screen.get_height()/2)
for i in range(startNum):
  creatures.append(Creature(randomColor(),[Layer(4, 5), Layer(5, 3), Layer(3, 2)]))
running = True
paused = False
clock = pygame.time.Clock()
startTime = datetime.datetime.now()
def pauseDef():
  global paused
  paused = not paused
pause = Button(10, 10, 200, 30, (255, 255, 255), "Pause/Unpause", pauseDef)
def exitDef():
  global running
  running = False
exitBut = Button(10, 40, 200, 30, (255, 255, 255), "Exit", exitDef)
print(startTime)
while running:
  clock.tick(300)
  # Events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      forever = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        paused = not paused
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_presses = pygame.mouse.get_pressed()
      if mouse_presses[0]:
        mouseXY = pygame.mouse.get_pos()
        pause.onclick(mouseXY[0], mouseXY[1])
        exitBut.onclick(mouseXY[0], mouseXY[1])
        for creature in creatures:
          if collision(creature.x, creature.y, creature.width, creature.width,
                       mouseXY[0], mouseXY[1], 1, 1):
            print(creature)
      if mouse_presses[2] and mouse_presses[1]:
        mouseXY = pygame.mouse.get_pos()
        energySource.x = mouseXY[0]
        energySource.y = mouseXY[1]
        energySource.initialx = mouseXY[0]
        energySource.initialy = mouseXY[1]
  # Render
  if paused == False:
    screen.fill("white")
    pause.draw()
    exitBut.draw()
    if energySource.w > 50:
      energySource.w -= 0.001
    if energySource.h > 50:
      energySource.h -= 0.001
    year += 0.001
    energySource.draw()
    creatures.sort(key=lambda x: x.energy, reverse=True)
    if len(creatures) == 0:
      running = False
    elif creatures[0].energy > highScorer["score"]:
      highScorer = {
        "desc": str(creatures[0]),
        "score": creatures[0].energy,
        "creature": creatures[0]
      }
    drawText(f"Population {len(creatures)} | Year: {round(year)} | FPS {round(clock.get_fps())} frames per second",
             screen.get_width() / 2, 10)
    for creature in creatures[:]:
      if creature.x < creature.width * 2 and creature in creatures:
        creature.x = creature.width * 2
        if year < 10 or year > 100:
          creatures.remove(creature)
        else:
          creature.energy -= 0.04
      elif creature.x + (creature.width * 2) > screen.get_width() and creature in creatures:
        creature.x = screen.get_width() - creature.width * 2
        if year < 10 or year > 100:
          creatures.remove(creature)
        else:
          creature.energy -= 0.04
      if creature.y < creature.width * 2 and creature in creatures:
        creature.y = creature.width * 2
        if year < 10 or year > 100:
          creatures.remove(creature)
        else:
          creature.energy -= 0.04
      elif creature.y + (creature.width * 2) > screen.get_height() and creature in creatures:
        creature.y = screen.get_height() - creature.width * 2
        if year < 10 or year > 100:
          creatures.remove(creature)
        else:
          creature.energy -= 0.04
      if len(creatures) < 50 and creature.age < 10:
        for layer in creature.network:
          layer.weights += 0.0001 * np.random.randn(layer.inputs, layer.neurons)
      creature.age += 0.001
      colided = collision(creature.x, creature.y, creature.width,
                          creature.width, energySource.rect[0],
                          energySource.rect[1], energySource.rect[2],
                          energySource.rect[3])
      if colided:
        creature.energy += creature.energyConsumption
      creature.energy -= creature.energyUsage
      if creature.energy >= 10:
        network = copy.deepcopy(creature.network)
        creature.energy = 5
        for layer in network:
          layer.weights += 0.01 * np.random.randn(layer.inputs, layer.neurons)
        creatures.append(Creature(creature.color, network))
        creatures[-1].x = creature.x
        creatures[-1].y = creature.y
      elif creature.energy <= 0.0:
        creatures.remove(creature)
      if creature.age > 160.0:
        creatures.remove(creature)
      creature.draw()
    pygame.display.flip()

end = datetime.datetime.now()
difference = end - startTime
seconds_in_day = 24 * 60 * 60
minutesSeconds = divmod(difference.days * seconds_in_day + difference.seconds, 60)
if highScorer["score"] > 0:
  print(highScorer['desc'])
  exitScene = True
  bestCreature = highScorer["creature"]
  bestCreature.width = 100
  bestCreature.x = 50
  bestCreature.y = 50
  while exitScene and forever == False:
    # Events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exitScene = False
    screen.fill("white")
    # Render
    bestCreature.draw(True)
    drawText(str(bestCreature), screen.get_width() / 2, 10, True, (0, 0, 0), 1)
    drawText(f"Simulation time: {minutesSeconds[0]} minutes, {minutesSeconds[1]} seconds.", screen.get_width() / 2, 25, True, (0, 0, 0), 1)
    pygame.display.flip()
if forever:
  os.execv(sys.executable, ['python'] + sys.argv)