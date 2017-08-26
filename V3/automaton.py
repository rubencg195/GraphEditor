import re

def getStateColor(state):
	colorGreen = '00'
	colorRed = '00'
	if (state.isInitial):
		colorGreen = 'ff'
	if (state.isFinal):
		colorRed = 'ff'
	color = "#" + colorRed + colorGreen + "00"
	return None if (color=="#000000") else color

class Automaton(object):
	def __init__(self, name, alphabet):
		super(Automaton, self).__init__()
		self.alphabet = alphabet
		self.name = name
		self.states = []

	def setAlphabet(self, alphabet):
		self.alphabet = alphabet

	def addState(self, state):
		self.states.append(state)

	def findState(self, stateName):
	  	for state in self.states:
	  		if state.label == stateName : 
	  			print("Find State ", state.label, " == ", stateName)
	  			return state
	  	return None

	def filter(self, stateName):
	  	stateList = []
	  	for state in self.states:
	  		if state.label == stateName:
	  			stateList.append( state )
	  	return stateList

	def addTransition(self, transition):
		_from = self.findState(self, transition._from)
		_from.addTransition(transition)

	def getInitialState(self):
		for state in self.states:
			if state.isInitial:
				return state

	def getFinalStates(self):
		finals = []
		for state in self.states:
			if state.isFinal:
				finals.append(state)
		return finals

	def toDataSet(self):
		nodes = []
		edges = []
		for state in self.states:
			stateInfo = {}
			stateInfo["nodeId"] = ""+("start" if state.isInitial else '')+"/"+("end" if state.isFinal else '') 
			stateInfo["id"]     = state.label
			stateInfo["label"]  = state.label
			stateInfo["color"]  = getStateColor(state)

			for edge in state.transitions:
				edgeInfo = {}
				edgeInfo["_from"] = edge._from
				edgeInfo["_to"]   = edge._to
				edgeInfo["label"] = edge.label
				edgeInfo["font"]  = {"align": "middle"}

				edges.append(edgeInfo)

			nodes.append(stateInfo)
		return ({"nodes": nodes, "edges":edges})

	def toData(self):
		nodes = []
		edges = []
		for state in self.states:
			stateInfo = {}
			stateInfo["isInitial"] = state.isInitial
			stateInfo["isFinal"]     = state.isFinal
			stateInfo["label"]  = state.label

			for edge in state.transitions:
				edgeInfo = {}
				edgeInfo["_from"] = edge._from
				edgeInfo["_to"]   = edge._to
				edgeInfo["label"] = edge.label

				edges.append(edgeInfo)

			nodes.append(stateInfo)
		return ({"nodes": nodes, "edges":edges})

	def toExampleLineFather(self, variableName, constructorName):
		dataset = self.toDataSet()
		for state in dataset["nodes"]:
			print(state)
		for edge in dataset["edges"]:
			print(edge)
       
class State(object):
	"""docstring for State"""
	def __init__(self, label="newState", isInitial=False, isFinal = False ):
		super(State, self).__init__()
		self.label = label
		self.isInitial = isInitial
		self.isFinal = isFinal
		self.transitions = []

		
	def addTransition(self, transition):
		self.transitions.append(transition)

	def setInitial(self, isInitial = True):
		this.isInitial = isInitial

	def setFinal(self, isFinal = False):
		this.isFinal = isFinal

	def hasTransition(self, symbol):
		for t in self.transitions:
			if len( re.findall(symbol, t) ) > 0 :
				return True
		return False

class Transition(object):
	"""docstring for Transition"""
	def __init__(self, label = "new Transition", _from = "_from", _to = "_to"):
		super(Transition, self).__init__()
		self.label = label
		self._from = _from
		self._to   = _to

	def match(self, a):
		setOfa = re.compile(",|\/").split(a)
		# print("Match ", setOfa)
		for e in re.compile(",|\/").split(self.label):
			for c in setOfa:
				if c == e:
					return True
		return False
		
	def ableToPop(self, symbol, popvalue):		
		values = self.label.split('/')
		leftValue  = values[0].split(',')
		rightValue = values[1].split(',')
		leftValue[0] == symbol and leftValue[1] == popvalue
