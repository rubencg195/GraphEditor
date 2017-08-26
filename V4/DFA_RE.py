from automaton import Automaton, State, Transition
from errors import UnknownCharError, UnknownStateError, DeterminismError, StateAlreadyExistError, NextTransitionError, AlreadyMinimizedError
import re
import string

class DFAre(Automaton):
	"""docstring for DFA"""
	def __init__(self, name, alphabet):
		Automaton.__init__(self, name, alphabet )

	def addState(self, stateName, isInitial = False, isFinal = False ):
		if not self.findState(stateName):
			self.states.append( State(stateName, isInitial, isFinal) )
		else:
			raise StateAlreadyExistError(stateName)
	def addTransition(self, transitionName, fromName, toName):
		_from = self.findState(fromName) #list( filter( lambda x: x.label == fromName, self.states ) )[0] #
		_to   = self.findState(toName)
		
		if not _from:
			raise UnknownStateError(fromName)
		if not _to:
			raise UnknownStateError(toName)
		if _from == _to:
			transitionName = transitionName

		existTransFromTo = None
		for x in _from.transitions:
			if x._to == toName:
				existTransFromTo = x
				break

		if existTransFromTo:
			existTransFromTo.label = '('+existTransFromTo.label+'+'+transitionName+')'
		else:
			_from.addTransition(Transition(transitionName, fromName, toName ))

	def getRegex(self):
		oneState = True if len( list( filter(lambda x: x.isInitial and x.isFinal, self.states ) ) ) > 0 else False
		
		if oneState:
			return self.toData()["edges"][0]["label"] + '*'
		else:
			initialState = self.getInitialState()
			finalState   = self.getFinalStates()[0]

			R = None
			S = None
			T = None
			U = None

			for x in initialState.transitions:
				if x._to == initialState.label:
					R = x
				if x._to == finalState.label:
					S = x

			for x in finalState.transitions:
				if x._to == finalState.label:
					T = x
				if x._to == initialState.label:
					U = x

			R = '('+R.label+')*' if R else ''
			S = S.label          if S else ''
			T = '('+T.label+')*' if T else ''
			U = U.label          if U else ''

			RST = R + ( '.' if R and S else '' ) + S + ( '.' if ( S and T or S and U ) else '' ) + T

			return '('+ RST + ('.' if T and U else '') + U+')*.'+ RST

	def toExampleLines(self):
		self.toExampleLinesFather('newDFAREautomaton', 'DFAre')
