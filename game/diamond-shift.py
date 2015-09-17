#!/usr/bin/env python
import sys
import pygame
from field import field

xoffset=11
yoffset=24
xcurs=0
ycurs=0

def separate_gems(gems):
  ng=[]
  size=gems.get_height()
  count=gems.get_width()/gems.get_height()
  for c in xrange(count):
    s= pygame.Surface((size,size),pygame.SRCALPHA, 32).convert_alpha()
    s.blit(gems,(0,0),pygame.Rect(c*size,0,(c+1)*size,size))
    #print pygame.Rect(c*size,0,(c+1)*size,size)
    #s=gems.subsurface(pygame.Rect(c*size,0,(c+1)*size,size))
    ng.append(s)
  return ng

pygame.init()
pygame.mouse.set_visible(0)
screen=pygame.display.set_mode((320,240),0,32)
gems=pygame.image.load("gems.png").convert_alpha()
bg=pygame.image.load("bg.png").convert_alpha()
gems=separate_gems(gems)
gemsize=gems[0].get_width()
grey=(75,75,75)
cursor=pygame.Surface((gemsize,gemsize)).convert_alpha()
cursor.fill(grey)
font = pygame.font.Font(None, 24)
score=0

def draw_field(s, gems, f):
  global gemsize
  size = gems[0].get_width()
  s.blit(bg,(0,0))
  s.blit(cursor, (xoffset + gemsize * xcurs, yoffset + gemsize * ycurs))
  for x in xrange(f.width):
    for y in xrange(f.height):
      s.blit(gems[f.map.get((x, y), 0)],(xoffset + x* size, yoffset + y * size))
  screen.blit(font.render("%d" % score, 1, (255, 255, 255)), (15, 3))
  pygame.display.flip()

f = field(8, 8, len(gems) - 1)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        sys.exit()
      if event.key ==  pygame.K_UP:
        if ycurs > 0:
          ycurs -= 1
      if event.key == pygame.K_DOWN:
        if ycurs < 7:
          ycurs += 1
      if event.key == pygame.K_LEFT:
        if xcurs > 0:
          xcurs -= 1
      if event.key == pygame.K_RIGHT:
        if xcurs < 7:
          xcurs += 1
      d = None
      if event.key == pygame.K_LCTRL:
        d = 'r'
      elif event.key == pygame.K_LSHIFT:
        d = 'l'
      elif event.key == pygame.K_SPACE:
        d = 'u'
      elif event.key == pygame.K_LALT:
        d = 'd'
      if d:
        f.swaps(xcurs, ycurs, d)
        draw_field(screen, gems, f)
        pygame.display.flip()
        pygame.time.delay(150)
        winners = f.find_winners()
        draw_field(screen, gems, f)
        pygame.display.flip()
        if winners:
          score += len(winners)
        else:
          f.swaps(xcurs, ycurs, d)
    while True:
      winners = f.find_winners()
      f.clear(winners)
      new_score = len(winners)
      draw_field(screen, gems, f)
      pygame.display.flip()
      if not new_score:
        break
      score+=new_score
      draw_field(screen, gems, f)
      loop = True
      while loop:
        loop = f.fall()
        loop = f.pour() or loop
        draw_field(screen, gems, f)
        pygame.display.flip()
        pygame.time.delay(150)
    pygame.display.flip()
