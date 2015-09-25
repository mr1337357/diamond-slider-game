#!/usr/bin/env python
import sys
import pygame
from field import field
from collections import namedtuple

class Point:
  def __init__(self, x = 0, y = 0):
    self.x = x
    self.y = y

class Control:
  def __init__(self, w, h):
    self.pos = Point(0,0)
    self.dim = Point(w,h)
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

ctrl = Control(7,7)

def separate_gems(gems):
  ng = []
  size = gems.get_height()
  count = gems.get_width()/gems.get_height()
  for c in xrange(count):
    s= pygame.Surface((size,size),pygame.SRCALPHA, 32).convert_alpha()
    s.blit(gems,(0,0),pygame.Rect(c*size,0,(c+1)*size,size))
    #print pygame.Rect(c*size,0,(c+1)*size,size)
    #s=gems.subsurface(pygame.Rect(c*size,0,(c+1)*size,size))
    ng.append(s)
  return ng

pygame.init()
pygame.mouse.set_visible(0)
screen = pygame.display.set_mode((320,240),0,32)
gems = pygame.image.load("gems.png").convert_alpha()
bg = pygame.image.load("bg.png").convert_alpha()
gems = separate_gems(gems)
gemsize = gems[0].get_width()
grey = (75,75,75)
cursor = pygame.Surface((gemsize,gemsize)).convert_alpha()
cursor.fill(grey)
font = pygame.font.Font(None, 24)
score = 0

def draw_field(s, gems, f, ctrl):
  xoffset = 11
  yoffset = 24
  #
  size = gems[0].get_width()
  s.blit(bg,(0,0))
  s.blit(cursor, (xoffset + gemsize * ctrl.pos.x, yoffset + gemsize * ctrl.pos.y))
  for x in xrange(f.width):
    for y in xrange(f.height):
      s.blit(gems[f.map.get((x, y), 0)],(xoffset + x * size, yoffset + y * size))
  screen.blit(font.render("%d" % score, 1, (255, 255, 255)), (15, 3))

f = field(8, 8, len(gems) - 1)

state = 'standby' # | swap | swap-back | fill | check | score
swap = None
winners = None

while not ctrl.quit:
  update(ctrl)
  delay = 16
  if state == 'standby':
    if ctrl.direction:
      swap = ctrl.pos, ctrl.direction
      state = 'swap'
  elif state == 'swap':
    f.swaps(swap[0].x, swap[0].y, swap[1])
    winners = f.find_winners()
    if winners:
      state = 'score'
    else:
      state = 'swap-back'
    delay = 150
  elif state == 'swap-back':
    f.swaps(swap[0].x, swap[0].y, swap[1])
    state = 'standby'
    delay = 150
  elif state == 'fill':
    again = f.fall()
    again = f.pour() or again
    if not again:
      state = 'check'
    delay = 150
  elif state == 'check':
    winners = f.find_winners()
    if winners:
      state = 'score'
    else:
      state = 'standby'
    delay = 150
  elif state == 'score':
    score += len(winners)
    f.clear(winners)
    state = 'fill'
    delay = 150
  draw_field(screen, gems, f, ctrl)
  pygame.display.flip()
  pygame.time.delay(delay)
