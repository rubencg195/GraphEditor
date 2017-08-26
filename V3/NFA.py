from automaton import Automaton, State, Transition
from DFA import DFA

from errors import UnknownCharError, UnknownStateError, DeterminismError, StateAlreadyExistError, NextTransitionError, AlreadyMinimizedError, NotValidWordError
import re
import string

class NFA(Automaton):
	"""docstring for NFA"""
	def __init__(self, name, alphabet):
		Automaton.__init__(self, name, alphabet )

	def addState(self, stateName, isInitial=False,isFinal = False ):
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
			_to = self.filter(toName)[0]
		except:
			raise UnknownStateError(toName)

		for c in re.compile(", | \/").split(transitionName):
			if not c in  self.alphabet:
				raise UnknownStateError(c)

		_from.addTransition(Transition(transitionName, fromName, toName))


	def match(self, w):
		finalState = self.matchState( w , self.getInitialState() )
		print("FinalState ", finalState)
		if not finalState:
			raise NotValidWordError(w)
		return finalState
		
	def matchState(self, w, currentState):
		print("MatchState currentState ", currentState.label, " word: ", w )

		if len(w) > 0:
			a = w[0]
			transitions = []
			for t in currentState.transitions:
				if t.match(a):
					print("Found trans ", t.label, " a: ",a )
					transitions.append(t)

			if len(transitions) > 0:
				statesTo = []
				for t in transitions:
					statesTo.append(self.findState(t._to))
				if len(statesTo) > 0:
					returnState = None
					for state in statesTo:
						if not returnState:
							returnState = self.matchState(w[1 : len(w)], state)
							if returnState != None and not returnState.isFinal:
								returnState = None
					return returnState
			else:
				return None
				# raise NextTransitionError(a, currentState.label)
		return currentState

	def toDFA(self):
		newStates = []
		initialState = self.getInitialState()
		newStates.append(initialState.label)

		alphabet = self.alphabet.split(',')
		stateTable = []
		x = 0
		stateTmp = ''
		for state in newStates:
			stateTable.append([None]*len(alphabet))
			y = 0
			for a in alphabet:
				print("ALPHAB ",a ," state ", state, " -- ", stateTmp )
				if stateTmp  != state:
					stateTo = getStateTo(self, state, a)
					if stateTo :
						print("YES")
						stateTmp = state
						stateTable[x][y] = stateTo
						newStates.append(stateTo)
				y = y + 1
			x = x + 1
		newDFA = DFA(self.name+"-toDFA", alphabet)
		newDFA.addState(normalizeState(newStates[0]), True)
		for i in range(1, len(newStates) ):
			newDFA.addState(normalizeState(newStates[i]), False, lookForFinal(self, newStates[i] ) )

		for i in range(len(stateTable)):
			for j in range(len(stateTable[i])):
				if(stateTable[i][j]):
					newDFA.addTransition(alphabet[j], normalizeState(newStates[i]), normalizeState(stateTable[i][j]) )

		return newDFA

	def toExampleLines(self):
		self.toExampleLinesFather("newNFAautomaton", "NFA")



def normalizeState(state):
	print("Normalize ", state)
	return "{"+state.replace('|' , ',')+"}"  #REVISAR ESTA LINEA!!!!

def getStateTo(nfa, state, a):
	statesTo = []
	statesLabels = state.split('|')
	print("getStateTo ", state, " -- ", a)
	for s in statesLabels:
		Astate = nfa.findState(s)

		if Astate:
			for t in list( filter( lambda x: x.match(a), Astate.transitions ) ):
				statesTo.append(nfa.findState(t._to).label)
	return '|'.join( statesTo )  #REVISAR ESTA LINEA!!!!

def lookForFinal(nfa, state):   #REVISAR ESTA FUNCION!!!!
	length = len( list( filter(lambda x: x.isFinal, list( map(lambda y: nfa.findState(y), state.split('|') ) ) ) ) ) > 0
	print("look for final length ", length)
	return length
