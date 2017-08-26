from automaton import Automaton, State, Transition

from DFA_RE import DFAre
from errors import UnknownCharError, UnknownStateError, DeterminismError, StateAlreadyExistError, NextTransitionError, AlreadyMinimizedError
import re
import string

contter = 0

class DFA(Automaton):
	"""docstring for DFA"""
	def __init__(self, name, alphabet):
		Automaton.__init__(self, name, alphabet )

	def addState(self, stateName, isInitial = False, isFinal = False ):
		# print("adding state ", stateName, isInitial, isFinal, self.findState(stateName))
		if not self.findState(stateName) :
			self.states.append(State(stateName, isInitial, isFinal))
		else:
			return
			# raise StateAlreadyExistError(stateName)

	def addTransition(self, transitionName, fromName, toName):
		# print("Adding Transition ", transitionName, " from ", fromName , " to ", toName)
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

		for c in re.compile(",|\/").split(transitionName):
			if c not in self.alphabet:
				raise UnknownCharError(c)

		if not(self.isDeterministic(_from, transitionName) ):
			raise DeterminismError(fromName, transitionName)

		existTransFromTo = None
		try:
			existTransFromTo = list(filter(lambda x: x._to == toName, _from.transitions ))[0]
		except:
			_from.addTransition( Transition(transitionName, fromName, toName) )


	def isDeterministic(self, _from, a):
		# print("isDet ", _from , a)
		length = len( list(filter(lambda e: e.label == a, _from.transitions ) ) )
		return not length

	def match(self, w):
		currentState = self.getInitialState()
		print("Evaluating Match, first State ", currentState.label)

		for a in w: 
			print("a: ",a, " w: ",w, " currentState ",currentState.label )
			nextTransition = None
			# nextTransition = list( filter(lambda e: e.label == a, self.states) )[0]
			for e in currentState.transitions:
				print("searching Trans a: ",a, " e: ",e.label)
				if e.match(a):
					nextTransition = e
					break

			if not nextTransition:
				raise NextTransitionError(a, currentState.label)

			currentState = self.findState(nextTransition._to)

		return currentState

	def generateDFA(self, state):
		dfa = DFA("selected final state: "+state.label, self.alphabet.split(',')  )
		for s in self.states:
			dfa.addState(s.label, s.isInitial, s.label == state.label)
		for s in self.states:
			for t in s.transitions:
				dfa.addTransition( t.label, t._from, t._to )
		return dfa

	def toRE( self ):
		automatons = self.toREstepByStep()
		print("toRE automatons  - ", len(automatons))
		regex = []

		for _as in automatons:
			print("t_as autom ", _as)
			a = _as[len(_as) - 1]
			regex.append('('+a.getRegex()+')')

		print("toRE finish  - ", '+'.join(regex))

		return {"regex": '+'.join(regex) , "stepByStep":automatons  }


	def toREstepByStep(self):
		finalStates = list( filter( lambda x: x.isFinal , self.states ) )
		automatons = []
		SetOfStepByStep = []

		for finalState in finalStates:
			print("fS in fSS ", finalState.label, "- ",len( self.generateDFA(finalState).states))
			automatons.append(self.generateDFA(finalState))
		for automaton in automatons:
			print("a in as ", self.regexFor(automaton))
			SetOfStepByStep.append(self.regexFor(automaton))

		return SetOfStepByStep

	def regexFor(self, dfa):
		stepByStep = []
		backAutomaton = DFAre(dfa.name+"-re", dfa.alphabet)
		stepByStep.append(backAutomaton)

		for state in dfa.states:
			backAutomaton.addState(state.label, state.isInitial, state.isFinal)
		for state in dfa.states:
			for trans in state.transitions:
				backAutomaton.addTransition(normalizeLabel(trans) , trans._from, trans._to)

		counter = 1 if len( list( filter( lambda x: not (x.isInitial or x.isFinal), backAutomaton.states ) ) ) > 0 else 2

		print("regex f counter ", counter, " - ", len( list( filter( lambda x: not (x.isInitial or x.isFinal), backAutomaton.states ) ) ))

		while( len(backAutomaton.states) > counter ):
			data = backAutomaton.toData()
			stateToDelete = None
			for n in data["nodes"]:
				if not (n["isInitial"] or n["isFinal"]):
					stateToDelete = n
			
			print("Entering while ",len(backAutomaton.states), " counter ", counter,  " stToDel ", stateToDelete )
					
			if(stateToDelete):
				fromEdges        = list(filter(lambda x: (x["_from"] == stateToDelete['label'] and x["_to"] != x["_from"]), data['edges'] ) )
				toEdges          = list(filter(lambda x: (x["_to"] == stateToDelete['label'] and x["_to"] != x["_from"]), data['edges'] ) )
				cerraduraEdges   = list(filter(lambda x: (x["_to"] == stateToDelete['label'] and x["_to"] == x["_from"]), data['edges'] ) )

				if cerraduraEdges:
					for edge in toEdges:
						edge["label"] = edge["label"] + '.('+cerraduraEdge["label"]+')*'

				currentAutomaton = DFAre("deleted state: "+stateToDelete['label'], backAutomaton.alphabet)

				for state in list( filter(lambda x: x["label"] != stateToDelete["label"] , data["nodes"] ) ) :
					currentAutomaton.addState( state["label"], state["isInitial"], state["isFinal"] )
					print("Sdding AU ", state["label"], " state to del ", stateToDelete["label"]) 

				for trans in list( filter(lambda x: (x["_from"] != stateToDelete["label"] and x["_to"] != stateToDelete["label"]) , data["edges"] ) ) :
					currentAutomaton.addTransition(trans["label"], trans["_from"], trans["_to"])

				for x in toEdges:
					for y in fromEdges:
						newLabel = x["label"] + '.' + y["label"]
						print("NEW LABEL ", newLabel)
						currentAutomaton.addTransition( newLabel, x["_from"], y["_to"] )

				stepByStep.append( currentAutomaton )
				backAutomaton = currentAutomaton
				print("Exiting while ",len(backAutomaton.states), " couAut ", len(currentAutomaton.states) )
			else:
				break

		print("ret stBSt ", stepByStep)

		return stepByStep

		def minimize( self ):
			global contter
			visitados = []
			equivalentes = []
			Noequivalentes = []
			colStates = self.states[1, len(self.states)   ]
			rowStates = self.states[0, len(self.states)-1 ]

			for col in colStates:
				for row in rowStates:
					contter = 0
					visitados = []
					print("top: "+col.label+' vs '+row.label)
					if col.label != row.label :
						self.DFS( col,row,visitados,equivalentes,Noequivalentes )

			minimized = self.mergeEquivalents(equivalentes)
			if len(minimized.states) == len(self.states):
				raise AlreadyMinimizedError(self.name)
			return minimized

		def DFS( self, Q, P, V, E, NE ):
			if self.areEquivalents(Q, P, V, E, NE):
				return
			NE.append( string.Join(',', [Q.label, P.label].sort() ) )

		def areEquivalents( self, Q,P,V,E,NE ):
			if Q.isFinal != P.isFinal :
				return False

			stateQ = self.findState( Q.label )
			stateP = self.findState( P.label )

			EQ = True
			lambdaResult = []

			print(Q.label + ' vs '+P.label)
			for a in self.alphabet:
				toQ = None
				toP = None
				for x in stateQ.transitions:
					if x.match(a):
						toQ = x
						break
				for x in stateP.transitions:
					if x.match(a):
						toP = x
						break

				if toQ and toP:
					toQ = self.findState( toQ._to )
					toP = self.findState( toP._to )

					print( "&("+Q.label+","+a+") = "+toQ.label )
					print( "&("+P.label+","+a+") = "+toP.label )

					EQ = EQ and toQ.label == toP.label
					lamdaResults.apend({"toQ": toQ,"toP":toP})
				elif toQ != toP:
					return False

			print('________________________')
			if EQ :
				E.append({ "Q1":Q, "Q2": P })
				return True
			for lr in lambdaResult:
				if lr["toQ"].label != lr["toP"].label:
					
					visitedTo = None
					for x in V:
						if (
								(x.Q.label == lr.toQ.label and x.P.label == lr.toP.label) or
								(x.Q.label == lr.toP.label and x.P.label == lr.toQ.label)
							):
							visitedTo = x;
					visitedTo = visitedTo != None or False

					for x in NE:
						if( x == string.Join(',', [lr.toQ.label,lr.toP.label].sort() ) ):
							return False
						elif visitedTo:
							continue
						else:
							V.append({'Q':Q, 'Q2':P})
							EQ = self.areEquivalents( lr.toQ,lr.toP,V,E,NE )
							if EQ:
								print("EQ: "+Q.label+' - '+P.label)
								E.append({'Q1':Q, 'Q2':P})
							else:
								return False
			return True

		def mergeEquivalents(self, E):
			automatonMin = DFA("minimized: "+self.name,self.alphabet.split(',') )
			newStates = []
			newStatesIndividualSet = []
			newTransitions = []

			i = 0
			while i < len(E):
				e = E[i]
				newState = []
				newState.append(e["Q1"].label) 
				newState.append(e["Q2"].label) 
				isStillInitial = e["Q1"].isInitial or e["Q2"].isInitial
				alreadyInNewStates = list( filter( lambda x: x.label == generateLabelNewState(newStatesIndividualSet, e["Q1"].label ) or x.label == generateLabelNewState(newStatesIndividualSet, e["Q2"].label), newStates) )
				if len(alreadyInNewStates) > 0:
					continue
				duplicated = self.getDuplicated(E, e)
				for d in duplicated:
					newState.append(d["Q1"].label )
					newState.append(d["Q2"].label )
					isStillInitial = isStillInitial or d["Q1"].isInitial and  d["Q2"].isInitial

					E = list(filter(lambda x: x["Q1"].label != d["Q1"].label and x["Q2"].label != d["Q2"].label ))

				newStatesIndividualSet.append(newState)
				newStateLabel = '{'+string.Join( '|', newState.sort() )+'}'
				newStates.append({"label":newStateLabel, "isInitial": isStillInitial, "isFinal": e["Q1"].isFinal })
				E = list( filter(lambda x: x["Q1"].label != e["Q1"].label and x["Q2"].label != e["Q2"].label  ) )
				#FUNCTION NOT FINISHED

		def getDuplicated(self, E, e):
			#FUNCTION NOT FINISHED
			pass

		def toExampleLines(self):
			self.toExampleLinesFather('newDFAautomaton', 'DFA')

def normalizeLabel(trans):
	satandBy = trans.label.replace('.','\\.').replace('+', "\\+").replace('*', '\\*')
	setOfChars = re.compile(',|\/').split(satandBy)
	if len(setOfChars) > 1:
		setOfChars = '('+ string.Join('+', setOfChars) +')'
	else:
		setOfChars = setOfChars[0]
	return setOfChars

def generateLabelNewState(newStatesIndividualSet, stateLabel):
	for newStateIndividual in newStatesIndividualSet:
		for ns in newStateIndividual:
			if ns == stateLabel:
				return '{'+string.Join( '|', newStatesIndividual.sort() )+'}'
	return None

def addNewTransition(newTransitions, newStatesIndividualSet, newStates, trans, fromLabel ):
	transSympols = re.compile(",|\/").split(trans.label)
	equivalent = None
	for ts in tranSymbols:
		equivalent = None
		for x in newStates:
			if x.label == generateLabelNewState(newStatesIndividualSet,trans.to):
				equivalent = x
		nt = None
		if equivalent:
			nt = {"label":ts, "_from":fromLabel, "_to": equivalent.label}
		else:
			nt = {"label":ts, "_from":fromLabel, "_to": trans.label}

		for x in newTransitions:
			if (
					x ["label"].index(nt["label"])>=0 or
					nt["label"].index( x["label"])>=0
				):
				newTransitions.append(nt)
				






