#!/usr/bin/env python
import pygame
from field import field

def separate_gems(gems):
  ng=[]
  size=gems.get_height()
  count=gems.get_width()/gems.get_height()
  for c in xrange(count):
    s= pygame.Surface((size,size)).convert_alpha()
    s.blit(gems,(0,0),pygame.Rect(c*size,0,(c+1)*size,size))
    ng.append(s)
  return ng

def drawcb(s,g,m):
  w=len(m)
  h=len(m[0])
  size=g[0].get_width()
  for x in xrange(w):
    for y in xrange(h):
      s.blit(gems[m[x][y]],(x*size,y*size))
  pygame.display.flip()

pygame.init()
screen=pygame.display.set_mode((320,240),0,32)
gems=pygame.image.load("gems.png").convert_alpha()
gems=separate_gems(gems)
gemsize=gems[0].get_width()
f = field(8,8,len(gems)-1,gems,screen,drawcb)
xcurs=0
ycurs=0
grey=(75,75,75)
cursor=pygame.Surface((gemsize,gemsize)).convert_alpha()
cursor.fill(grey)
while f.check_for_winners():
  f.fill()
while 1:
  while f.check_for_winners():
    f.fill()
  screen.fill(0)
  screen.blit(cursor,(gemsize*xcurs,gemsize*ycurs))
  f.redraw()
  screen.blit(cursor,(gemsize*xcurs,gemsize*ycurs))
  pygame.display.flip()
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      import sys; sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        import sys; sys.exit()
      if event.key ==  pygame.K_UP:
        if ycurs > 0:
          ycurs -= 1
      if event.key == pygame.K_DOWN:
        if ycurs < 8:
          ycurs += 1
      if event.key == pygame.K_LEFT:
        if xcurs > 0:
          xcurs -= 1
      if event.key == pygame.K_RIGHT:
        if xcurs < 7:
          xcurs += 1
      if event.key == pygame.K_LCTRL:
        f.check_swap(xcurs,ycurs,'r')
      if event.key == pygame.K_LSHIFT:
        f.check_swap(xcurs,ycurs,'l')
      if event.key == pygame.K_SPACE:
        f.check_swap(xcurs,ycurs,'u')
      if event.key == pygame.K_LALT:
        f.check_swap(xcurs,ycurs,'d')
