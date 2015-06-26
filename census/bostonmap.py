
grid = None

cutoff = 1.0

def initGrid():
  return 

def loadParcels():
  return

def test():
  return

def distance(parcel, datum):
  return 

class BinGrid(object):
  def __init__(self, xmin, xmax, ymin, ymax, binsize):
    self.grid = {}
    for i in range(xmin, xmax, binsize):
      self.grid[i] = {}
      for j in range(ymin, ymax, binsize):
        self.grid[i][j] = []
    return

  def add(self, datum):
    global cutoff
    i = int(float(datum['lon']))/binsize
    j = int(float(datum['lon']))/binsize
    for p in self.grid[i][j]:
      if distance(p, datum) <= cutoff:
        p.append(datum)

if __name__ == "__main__":
  test()