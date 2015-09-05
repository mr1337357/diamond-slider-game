import random
import pygame

# game field
# 2D list with numbers representing gem types
# index as filed[x][y] where x is steps from left, y is steps from top

def donothing(*args,**kwargs):
  pass

class field(object):
  def __init__(self,width,height,ngems,gems=None,screen=None,drawcb=None):
    self.screen=screen
    self.gems=gems
    self.ngems=ngems
    self.width=width
    self.height=height
    self.map=[ [0]*height for i in xrange(width)]
    self.drawcb=drawcb
    if not drawcb:
      self.drawcb=donothing
    self.fill()

  def fill(self):
    done=False
    while not done:
      done=True
      for x in xrange(self.width):
        for y in reversed(xrange(1,self.height,1)):
          if self.map[x][y]==0:
            done=False
            self.map[x][y]=self.map[x][y-1]
            self.map[x][y-1]=0
      for x in xrange(self.width):
        if self.map[x][0] == 0:
          done=False
          self.map[x][0] = random.randint(1,self.ngems)
      self.drawcb(self.screen,self.gems,self.map)
      pygame.time.delay(100)
  
  def check_for_winners(self):
    done=False
    r=False
    while not done:
      rmmap=[ [0]*self.height for i in xrange(self.width)]
      done=True
      for x in xrange(self.width):
        for y in xrange(self.height):
          if y < self.height-2:
            if self.map[x][y] == self.map[x][y+1] == self.map[x][y+2]:
              rmmap[x][y]=1
              rmmap[x][y+1]=1
              rmmap[x][y+2]=1
          if x < self.width-2:
            if self.map[x][y] == self.map[x+1][y] == self.map[x+2][y]:
              rmmap[x][y]=1
              rmmap[x+1][y]=1
              rmmap[x+2][y]=1
      for x in xrange(self.width):
        for y in xrange(self.height):
          if rmmap[x][y]:
            r = True
            self.map[x][y] = 0
    self.screen.fill(0)
    self.redraw()
    pygame.display.flip()
    return r

  def redraw(self):
    self.drawcb(self.screen,self.gems,self.map)

  def check_swap(self,x,y,d):
    if d == 'u':
      if y == 0:
        return
      t=self.map[x][y]
      self.map[x][y]=self.map[x][y-1]
      self.map[x][y-1]=t
    
    if d == 'd':
      if y == 7:
        return
      t=self.map[x][y]
      self.map[x][y]=self.map[x][y+1]
      self.map[x][y+1]=t
    
    if d == 'l':
      if x == 0:
        return
      t=self.map[x][y]
      self.map[x][y]=self.map[x-1][y]
      self.map[x-1][y]=t
    if d == 'r':
      if x == 7:
        return
      t=self.map[x][y]
      self.map[x][y]=self.map[x+1][y]
      self.map[x+1][y]=t
    
      
    self.screen.fill(0)
    self.redraw()
    pygame.display.flip()
    pygame.time.delay(150)
    if self.check_for_winners():
      return
    if d == 'u':
      t=self.map[x][y]
      self.map[x][y]=self.map[x][y-1]
      self.map[x][y-1]=t
      
    if d == 'd':
      t=self.map[x][y]
      self.map[x][y]=self.map[x][y+1]
      self.map[x][y+1]=t
      
    if d == 'l':
      t=self.map[x][y]
      self.map[x][y]=self.map[x-1][y]
      self.map[x-1][y]=t
      
    if d == 'r':
      t=self.map[x][y]
      self.map[x][y]=self.map[x+1][y]
      self.map[x+1][y]=t
