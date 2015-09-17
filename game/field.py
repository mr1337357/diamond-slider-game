import random
import pygame

# game field
# 2D list with numbers representing gem types
# index as field[x][y] where x is steps from left, y is steps from top

class field(object):
  def __init__(self, width, height, ngems):
    self.ngems = ngems
    self.width = width
    self.height = height
    self.map = {}
    self.fill()

  def clear(self, winners):
    for winner in winners:
      self.place(winner[0], winner[1], None)

  def fill(self):
    loop = True
    while loop:
      self.clear(self.find_winners())
      loop = self.fall()
      loop = self.pour() or loop

  def place(self, x, y, v):
    if v is None:
      if (x, y) in self.map:
        del self.map[x, y]
    else:
       self.map[x, y] = v

  def fall(self):
    fell = False
    for x in xrange(self.width):
      for y in reversed(xrange(1, self.height,1)):
        if not (x,y) in self.map:
          fell = True
          self.place(x, y, self.map.get((x, y - 1)))
          self.place(x, y - 1, None)
    return fell
        
  def pour(self):
    poured = False
    for x in xrange(self.width):
      if not (x, 0) in self.map:
        poured = True
        self.map[x, 0] = random.randint(1, self.ngems)
    return poured

  def find_winners(self):
    # TODO: needs BFS to check for an area of 3+
    winners = set()
    for x in xrange(self.width):
      for y in xrange(self.height):
        if y < self.height - 2:
          if self.map.get((x, y)) == self.map.get((x, y + 1)) == self.map.get((x, y + 2)):
            winners.add((x, y))
            winners.add((x, y + 1))
            winners.add((x, y + 2))
        if x < self.width - 2:
          if self.map.get((x, y)) == self.map.get((x + 1, y)) == self.map.get((x + 2, y)):
            winners.add((x, y))
            winners.add((x + 1, y))
            winners.add((x + 2, y))
    return winners

  def swaps(self, x, y, d):
    def swap(u, v):
      a, b = x + u, y + v
      t = self.map.get((x, y))
      s = self.map.get((a, b))
      self.place(x, y, s)
      self.place(a, b, t)
    if d == 'u' and y > 0:
      swap(0, -1)
    if d == 'd' and y < self.height - 1:
      swap(0, 1)
    if d == 'l' and x > 0:
      swap(-1, 0)
    if d == 'r' and x < self.width - 1:
      swap(1, 0)
