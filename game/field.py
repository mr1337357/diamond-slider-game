import random
import pygame

# game field
# 2D list with numbers representing gem types
# index as filed[x][y] where x is steps from left, y is steps from top

def donothing(*args,**kwargs):
  pass

def empty_map(w,h):
  return dict.fromkeys(sum(map(lambda x: zip([x] * 10, range(10)), range(10)), []), None)

class field(object):
  def __init__(self,width,height,ngems,gems=None,screen=None,drawcb=None):
    self.screen=screen
    self.gems=gems
    self.ngems=ngems
    self.width=width
    self.height=height
    self.map=empty_map(width, height)
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
          if not self.map.get((x,y)):
            done=False
            self.map[x,y]=self.map.get((x,y-1))
            self.map[x,y-1]=None
      for x in xrange(self.width):
        if not self.map.get((x,0)):
          done=False
          self.map[x,0] = random.randint(1,self.ngems)
      self.drawcb(self.screen,self.gems,self.map,self.width,self.height)
      pygame.time.delay(100)
  
  def check_for_winners(self):
    done=False
    r=False
    while not done:
      rmmap=empty_map(self.width, self.height)
      done=True
      for x in xrange(self.width):
        for y in xrange(self.height):
          if y < self.height-2:
            if self.map.get((x,y)) == self.map.get((x,y+1)) == self.map.get((x,y+2)):
              rmmap[x,y]=1
              rmmap[x,y+1]=1
              rmmap[x,y+2]=1
          if x < self.width-2:
            if self.map.get((x,y)) == self.map.get((x+1,y)) == self.map.get((x+2,y)):
              rmmap[x,y]=1
              rmmap[x+1,y]=1
              rmmap[x+2,y]=1
      for x in xrange(self.width):
        for y in xrange(self.height):
          if rmmap.get((x,y)):
            r = True
            self.map[x,y] = None
    #self.screen.fill(0)
    self.redraw()
    pygame.display.flip()
    return r

  def redraw(self):
    self.drawcb(self.screen,self.gems,self.map,self.width,self.height)

  def check_swap(self,x,y,d):
    def swap(u, v, ok=True):
      if ok:
        t=self.map.get((x,y))
        self.map[x,y]=self.map.get((x+u,y+v))
        self.map[x+u,y+v]=t

    if d == 'u':
      swap(0, -1, y > 0)
    if d == 'd':
      swap(0, 1, y < 7)
    if d == 'l':
      swap(-1, 0, x > 0)
    if d == 'r':
      swap(1, 0, x < 7)
      
    self.redraw()
    pygame.display.flip()
    pygame.time.delay(150)
    if self.check_for_winners():
      return

    if d == 'u':
      swap(0, -1)
    if d == 'd':
      swap(0, 1)
    if d == 'l':
      swap(-1, 0)
    if d == 'r':
      swap(1, 0)
