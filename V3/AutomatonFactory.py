
from DFA  import DFA
from NFA  import NFA
from NFA-e import NFAe
from PDA  import PDA

seed = 0
steps = 0
epsilon = "epsilon"

def newQ():
	global seed
	tmp = seed
	seed = seed + 1
	return tmp 

def nexStep():
	global steps
	tmp = steps
	steps = steps++
	return tmp
	
