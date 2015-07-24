import cPickle as cp
import math

# author: Hayden Fuss
# last edited: Thursday, July 23, 2015
# source for poissonProb: http://onlinestatbook.com/2/probability/poisson.html

keys = ['medical', 'violent', 'petty', 'unsorted']
avgs = {}

for k in keys:
  with open(k + '_avgs.pkl', 'rb') as f:
    avgs[k] = cp.load(f)

def poissonProb(dispatches, ct, latent):
  global avgs
  avg = avgs[latent][ct]
  return math.exp(-avg)*(avg**dispatches)/(math.factorial(dispatches))