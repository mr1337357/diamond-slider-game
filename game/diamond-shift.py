#!/usr/bin/env python
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

def gem_idx(idx):
  if idx is None:
    return 0
  return idx

def drawcb(s,g,m,w,h):
  global gemsize
  size=g[0].get_width()
  s.blit(bg,(0,0))
  s.blit(cursor,(xoffset+gemsize*xcurs,yoffset+gemsize*ycurs))
  for x in xrange(w):
    for y in xrange(h):
      s.blit(gems[gem_idx(m.get((x,y), 0))],(xoffset+x*size,yoffset+y*size))
  pygame.display.flip()



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
f = field(8,8,len(gems)-1,gems,screen,drawcb)

while f.check_for_winners():
  f.fill()
while 1:
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
        if ycurs < 7:
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
    while f.check_for_winners():
      f.fill()
    f.redraw()
    #screen.blit(cursor,(gemsize*xcurs,gemsize*ycurs))
    pygame.display.flip()
