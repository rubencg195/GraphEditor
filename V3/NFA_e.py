from automaton import Automaton, State, Transition

from DFA import DFA
from errors import UnknownCharError, UnknownStateError, DeterminismError, StateAlreadyExistError, NextTransitionError, AlreadyMinimizedError,NotValidWordError
import re
import string

epsilon = 'E'

class NFAe(Automaton):
	"""docstring for DFA"""
	def __init__(self, name, alphabet):
		Automaton.__init__(self, name, alphabet)
	
	def addState(self, stateName, isInitial = False, isFinal = False ):
		if not self.findState(stateName):
			self.states.append(State(stateName, isInitial, isFinal))
		else:
			raise StateAlreadyExistError(stateName)

	def addTransition(self, transitionName, fromName, toName):
		_from = None
		_to   = None
		try:
			_from = self.filter(fromName)[0]
		except:
			raise UnknownStateError(fromName)
		try:
			_to   = self.filter(toName)[0]
		except:
			raise UnknownStateError(toName)
		for c in re.compile(", | \/").split(transitionName):
			if not c in self.alphabet and c != epsilon:
				raise UnknownCharError(c)
		_from.addTransition(Transition(transitionName, fromName, toName))


	def clausura(self, state):
		print('Check if Claus ', state.label)
		states = []
		states.append(state)

		for f in list(filter(lambda x: x.match(epsilon), state.transitions)):
			print('Yes Claus ', state.label)
			epsilonState = self.findState(f._to)
			states.append(epsilonState)
			states = states + self.clausura(epsilonState) 

		return states

	def match(self, w):
		finalState = self.matchStates(w, [self.getInitialState()])
		print("Final State ", finalState)
		if not finalState:
			raise NotValidWordError(w)
		return finalState

	def matchStates(self,  w , currentStates ):

		clausuras = []
		for currentState in currentStates:
			print("MatchState currentState ", currentState.label, " word: ", w )

			tempClausuras = self.clausura(currentState)
			for claus in tempClausuras:
				clausuras.append(claus)

		if len(w) > 0:
			a = w[0]
			statesTo = []

			for claus in clausuras:
				transitions = list(filter(lambda x: x.match(a), claus.transitions ))
				for t in transitions:
					print("append Trans ", t.label)
					statesTo.append(self.findState(t._to))

			if len(statesTo) == 0:
				raise NextTransitionError(a, '('+','.join( map(lambda x: x.label , currentStates) )+')' )
			return self.matchStates( w[ 1 : len(w) ], statesTo )

		return list( filter(lambda x: x.isFinal, clausuras) )[0]

	def toDFA(self):
		newStates = []
		initialState = self.getInitialState()
		newStates.append( '|'.join( list( map(lambda x: x.label, self.clausura(initialState) ) ) ) )

		alphabet = self.alphabet.split(',')
		stableTable = []

		x = 0
		for state in newStates:
			stableTable.append([None]*len(alphabet))
			y = 0
			for a in alphabet:
				stateTo = getStateTo(self, state, a)

				if(stateTo):
					stableTable[x][y] = stateTo
					newStates.append(stateTo)
				y = y+1
			x = x+1

		newDFA = DFA(self.name+"-toDFA", alphabet)
		newDFA.addState(normalizeState(newStates[0]), True)
		for i in range(1, len(newStates)):
			newDFA.addState(normalizeState(newStates[i]), False, lookForFinal(self, newStates[i]))

		for i in range( len(newStates) ):
			for j in range( len(stableTable[i]) ):
				if(stableTable[i][j]):
					newDFA.addTransition(alphabet[j], normalizeState(newStates[i]), normalizeState( stableTable[i][j]) )

		return newDFA

	def toExampleLines(self):
		self.toExampleLinesFather("newNFAautomaton", "NDAe")

def normalizeState(state):
	return "{" + state.replace('|', ',') + '}'

def getStateTo(nfae, state, a):
	stateTo = []
	statesLabels = state.split('|')
	for s in statesLabels:
		Astate = nfae.findState(s)
		if Astate:
			for  t in list(filter(lambda x: x.match(a), Astate.transitions)):
				for c in list( map( lambda x: x.label , nfae.clausura(nfae.findState(t._to)) ) ):
					stateTo.append(c)

	return '|'.join( stateTo )

def lookForFinal(nfae, state):
	return len( list( filter( lambda y: y.isFinal ,list( map( lambda x: nfae.findState(x),  state.split('|') ) ) ) ) ) > 0