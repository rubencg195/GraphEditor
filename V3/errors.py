from PyQt4 import QtCore, QtGui

class ValidationError(Exception):
    def __init__(self, message, errors):
        super(ValidationError, self).__init__(message)
        showMsg(message)

class UnknownCharError(Exception):
    def __init__(self, unknownChar):
        message = "Character " + unknownChar +" is not a part of the alphabet."
        super(UnknownCharError, self).__init__(message)
        showMsg(message)

class UnknownStateError(Exception):
    def __init__(self, stateName):
        message = "State "+stateName+" does not exist in the automata."
        super(UnknownStateError, self).__init__(message)
        showMsg(message)

class StateAlreadyExistError(Exception):
    def __init__(self, stateName):
        message = "State "+stateName+" already exist in the automata."
        super(StateAlreadyExistError, self).__init__(message)
        showMsg(message)
    

class DeterminismError(Exception):
    def __init__(self, state, a):
        message = "State "+state+" already has a transition with character "+a+"."
        super(DeterminismError, self).__init__(message)
        showMsg(message)

class NextTransitionError(Exception):
    def __init__(self, transition, q = ''):
        message = "Transition "+transition+" in "+q +" not exist."
        super(NextTransitionError, self).__init__(message)
        showMsg(message)


class AlreadyMinimizedError(Exception):
    def __init__(self, name):
        message = "The automaton: "+name+" is already minimized."
        super(AlreadyMinimizedError, self).__init__(message)
        showMsg(message)

class NotValidWordError(Exception):
    def __init__(self, word):
        message = "The word: "+word+" is not valid." 
        super(NotValidWordError, self).__init__(message)
        showMsg(message)

def showMsg(text):
  msgBox = QtGui.QMessageBox( None )
  msgBox.setIcon( QtGui.QMessageBox.Information )
  msgBox.setText( text )
  msgBox.addButton( QtGui.QMessageBox.Yes )
  msgBox.setDefaultButton( QtGui.QMessageBox.Yes ) 
  ret = msgBox.exec_()