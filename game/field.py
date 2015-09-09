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
    self.map={}
    self.drawcb=drawcb
    if not drawcb:
      self.drawcb=donothing
    self.fill()

  def place(self, x, y, v):
    if v is None:
      if (x,y) in self.map:
        del self.map[x,y]
    else:
       self.map[x,y]=v

  def fill(self):
    done=False
    while not done:
      done=True
      # apply gravity
      for x in xrange(self.width):
        for y in reversed(xrange(1,self.height,1)):
          if not (x,y) in self.map:
            done=False
            self.place(x,y,self.map.get((x,y-1)))
            self.place(x,y-1,None)
      # fill the top row
      for x in xrange(self.width):
        if not (x,0) in self.map:
          done=False
          self.map[x,0] = random.randint(1,self.ngems)
      self.drawcb(self.screen,self.gems,self.map,self.width,self.height)
      pygame.time.delay(100)

  def check_for_winners(self):
    winners=0
    rmmap={}
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
        if (x,y) in rmmap:
          winners+=1
          self.place(x,y,None)
    #self.screen.fill(0)
    self.redraw()
    pygame.display.flip()
    return winners

  def redraw(self):
    self.drawcb(self.screen,self.gems,self.map,self.width,self.height)

  def check_swap(self,x,y,d):
    def swap(u, v):
      t=self.map.get((x,y))
      s=self.map.get((x+u,y+v))
      self.place(x,y,s)
      self.place(x+u,y+v,t)
    def swaps():
      if d == 'u' and y > 0:
        swap(0, -1)
      if d == 'd' and y < 7:
        swap(0, 1)
      if d == 'l' and x > 0:
        swap(-1, 0)
      if d == 'r' and x < 7:
        swap(1, 0)
    swaps()    
    self.redraw()
    pygame.display.flip()
    pygame.time.delay(150)
    winners=self.check_for_winners()
    if winners:
      return winners
    swaps()
    return 0
