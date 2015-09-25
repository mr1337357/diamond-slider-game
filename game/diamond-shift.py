#!/usr/bin/env python
import sys
import pygame
from field import Field
from copy import deepcopy

class Point:
  def __init__(self, x = 0, y = 0):
    self.x = x
    self.y = y
  def __repr__(self):
    return repr((self.x, self.y))

class Control:
  def __init__(self, dim):
    self.pos = Point(0,0)
    self.dim = dim
    self.direction = None
    self.quit = False

def update(ctrl):
  ctrl.direction = None
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      ctrl.quit = True
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        ctrl.quit = True
      if event.key ==  pygame.K_UP:
        if ctrl.pos.y > 0:
          ctrl.pos.y -= 1
      if event.key == pygame.K_DOWN:
        if ctrl.pos.y < ctrl.dim.y:
          ctrl.pos.y += 1
      if event.key == pygame.K_LEFT:
        if ctrl.pos.x > 0:
          ctrl.pos.x -= 1
      if event.key == pygame.K_RIGHT:
        if ctrl.pos.x < ctrl.dim.x:
          ctrl.pos.x += 1
      if event.key == pygame.K_LCTRL:
        ctrl.direction = 'r'
      elif event.key == pygame.K_LSHIFT:
        ctrl.direction = 'l'
      elif event.key == pygame.K_SPACE:
        ctrl.direction = 'u'
      elif event.key == pygame.K_LALT:
        ctrl.direction = 'd'

class DiamondShift:
  def __init__(self):
    pygame.init()
    pygame.mouse.set_visible(0)
    self.screen = pygame.display.set_mode((320, 240), 0, 32)
    self.gems = pygame.image.load("gems.png").convert_alpha()
    self.bg = pygame.image.load("bg.png").convert_alpha()
    self.gems = self.separate_gems(self.gems)
    self.gemsize = self.gems[0].get_width()
    self.grey = (75, 75, 75)
    self.cursor = pygame.Surface((self.gemsize, self.gemsize)).convert_alpha()
    self.cursor.fill(self.grey)
    self.font = pygame.font.Font(None, 24)
    self.score = 0
    self.field = Field(8, 8, len(self.gems) - 1)
    self.ctrl = Control(Point(7, 7))
    self.state = 'standby' # | swap | swap-back | fill | check | score
    self.swap = None 
    self.winners = None

  def run(self):
    while self.loop():
      self.read()
      self.step()
      # self.draw()

  def loop(self):
    return not self.ctrl.quit

  def read(self):
    update(self.ctrl)

  def step(self):
    delay = 16

    if self.state == 'standby':
      if self.ctrl.direction:
        self.swap = deepcopy((self.ctrl.pos, self.ctrl.direction))
        self.state = 'swap'
  
    elif self.state == 'swap':
      self.field.swaps(self.swap[0].x, self.swap[0].y, self.swap[1])
      self.winners = self.field.find_winners()
      if self.winners:
        self.state = 'score'
      else:
        self.state = 'swap-back'
      delay = 150
      
    elif self.state == 'swap-back':
      self.field.swaps(self.swap[0].x, self.swap[0].y, self.swap[1])
      self.state = 'standby'
      delay = 150
      
    elif self.state == 'fill':
      again = self.field.fall()
      again = self.field.pour() or again
      if not again:
        self.state = 'check'
      delay = 150
      
    elif self.state == 'check':
      self.winners = self.field.find_winners()
      if self.winners:
        self.state = 'score'
      else:
        self.state = 'standby'
      delay = 150
      
    elif self.state == 'score':
      self.score += len(self.winners)
      self.field.clear(self.winners)
      self.state = 'fill'
      delay = 150

    self.draw()
    pygame.time.delay(delay)

  def draw(self):
    xoffset = 11
    yoffset = 24
    size = self.gems[0].get_width()
    self.screen.blit(self.bg,(0,0))
    self.screen.blit(self.cursor, (xoffset + self.gemsize * self.ctrl.pos.x, yoffset + self.gemsize * self.ctrl.pos.y))
    for x in xrange(self.field.width):
      for y in xrange(self.field.height):
        self.screen.blit(self.gems[self.field.map.get((x, y), 0)],(xoffset + x * size, yoffset + y * size))
    self.screen.blit(self.font.render("%d" % self.score, 1, (255, 255, 255)), (15, 3))
    pygame.display.flip()

  def separate_gems(self, gems):
    ng = []
    size = self.gems.get_height()
    count = self.gems.get_width()/gems.get_height()
    for c in xrange(count):
      s = pygame.Surface((size,size),pygame.SRCALPHA, 32).convert_alpha()
      s.blit(self.gems, (0, 0), pygame.Rect(c * size, 0, (c + 1) * size, size))
      ng.append(s)
    return ng

game = DiamondShift()
game.run()
