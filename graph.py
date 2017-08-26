# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import sys
import json
from random import randint
from PyQt4 import QtCore, QtGui

from fysom import Fysom
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA


app = QtGui.QApplication(sys.argv)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

currNode = None
nextNode = None
nodeList = []
conList = []

painter = None
canvas = None
mainWidget = None
mode = "NFA"
action = ""

startNode = None
evalValue = None

symbols = {'0', '1'}


class Canvas(QtGui.QWidget):
    def __init__(self, parent):
      QtGui.QWidget.__init__(self, parent)

    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        for con in conList:
          qp.setPen(QtGui.QColor(con.red , con.green , con.blue))
          pen = qp.pen()
          pen.setWidth(5)
          qp.setPen(pen)
          qp.setFont(QtGui.QFont('Decorative', 20))
          # print con.node.name , " to ", con.nextNode.name , " node " ,con.name
          x1 = con.node.x()
          y1 = con.node.y()
          x2 = con.nextNode.x()
          y2 = con.nextNode.y()

          try:
            if(not con.node.deleted and not con.nextNode.deleted):
              if(con.node != con.nextNode):
                qp.drawLine(x1+25, y1+25, x2+25 , y2+25 )
                slope =   ( y2 - y1 ) / ( x2 - x1 ) 
                factor = -15
                factorX =  slope * factor
                factorY =  slope * factor 
                qp.drawText(QtCore.QPoint( x2 + factorX , y2 + factorY ) , con.name ) 
              else:
                qp.drawEllipse(con.node.x() - 25 , con.node.y() - 25 , 50 , 50 )
                factorX = -50
                factorY = -50
                qp.drawText(QtCore.QPoint( x2 + factorX , y2 + factorY ) , con.name ) 
            else:
              print( "alguno es nulo")
              if(con.node.deleted):
                con.delCon(con.nextNode)
              if(con.nextNode.deleted):
                con.delCon(con.node)
          except:
            pass 
            
        qp.end()
        


class Ui_MainWindow(QtGui.QWidget):
    def __init__(self):
      QtGui.QWidget.__init__(self)
    def setupUi(self):
      self.setObjectName(_fromUtf8("MainWindow"))
      self.resize(1500, 900)
      self.menu = QtGui.QWidget(self)
      self.menu.setGeometry(QtCore.QRect(10, 10, 251, 900))
      self.menu.setObjectName(_fromUtf8("menu"))
      self.pushButton_edit = QtGui.QPushButton(self.menu)
      self.pushButton_edit.setGeometry(QtCore.QRect(10, 536, 221, 51))
      self.pushButton_edit.setObjectName(_fromUtf8("pushButton_edit"))
      self.pushButton_delete = QtGui.QPushButton(self.menu)
      self.pushButton_delete.setGeometry(QtCore.QRect(10, 596, 221, 51))
      self.pushButton_delete.setObjectName(_fromUtf8("pushButton_delete"))
      self.pushButton_add = QtGui.QPushButton(self.menu)
      self.pushButton_add.setGeometry(QtCore.QRect(10, 476, 221, 51))
      self.pushButton_add.setObjectName(_fromUtf8("pushButton_add"))

      self.comboBox_type = QtGui.QComboBox(self.menu)
      self.comboBox_type.setGeometry(QtCore.QRect(10, 30, 221, 51))
      self.comboBox_type.setObjectName(_fromUtf8("comboBox_type"))
      self.comboBox_type.addItem(_fromUtf8(""))
      self.comboBox_type.addItem(_fromUtf8(""))
      self.comboBox_type.addItem(_fromUtf8(""))

      self.comboBox_edit_type = QtGui.QComboBox(self.menu)
      self.comboBox_edit_type.setGeometry(QtCore.QRect(10, 90, 221, 51))
      self.comboBox_edit_type.setObjectName(_fromUtf8("comboBox_type"))
      self.comboBox_edit_type.addItem("NODE")
      self.comboBox_edit_type.addItem("CONNECTION")



      self.label_con = QtGui.QLabel("Node Connections", self.menu)
      self.label_con.setGeometry(QtCore.QRect(90, 150, 68, 17))
      self.comboBox_con = QtGui.QComboBox(self.menu)
      self.comboBox_con.setGeometry(QtCore.QRect(10, 190, 221, 51))
      self.pushButton_deselect = QtGui.QPushButton("Deselect", self.menu)
      self.pushButton_deselect.setGeometry(QtCore.QRect(10, 250, 221, 61))
      self.pushButton_deselect.setObjectName(_fromUtf8("pushButton_con"))

      self.label = QtGui.QLabel(self.menu)
      self.label.setGeometry(QtCore.QRect(100, 390, 68, 17))
      self.label.setObjectName(_fromUtf8("label"))
      self.lineEdit_value = QtGui.QLineEdit(self.menu)
      self.lineEdit_value.setGeometry(QtCore.QRect(20, 346, 211, 41))
      self.lineEdit_value.setObjectName(_fromUtf8("lineEdit_value"))
      self.label_2 = QtGui.QLabel(self.menu)
      self.label_2.setGeometry(QtCore.QRect(90, 320, 68, 17))
      self.label_2.setObjectName(_fromUtf8("label_2"))

      self.pushButton_save = QtGui.QPushButton(self.menu)
      self.pushButton_save.setGeometry(QtCore.QRect(10, 746, 221, 61))
      self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))

      self.pushButton_load = QtGui.QPushButton("Load",self.menu)
      self.pushButton_load.setGeometry(QtCore.QRect(10, 810, 221, 61))
      self.pushButton_load.setObjectName(_fromUtf8("pushButton_load"))

      self.label_3 = QtGui.QLabel(self.menu)
      self.label_3.setGeometry(QtCore.QRect(40, 670, 161, 20))
      self.label_3.setObjectName(_fromUtf8("label_3"))
      self.lineEdit_filename = QtGui.QLineEdit(self.menu)
      self.lineEdit_filename.setGeometry(QtCore.QRect(10, 700, 221, 41))
      self.lineEdit_filename.setObjectName(_fromUtf8("lineEdit_filename"))
      self.label_4 = QtGui.QLabel(self.menu)
      self.label_4.setGeometry(QtCore.QRect(100, 10, 68, 17))
      self.label_4.setObjectName(_fromUtf8("label_4"))
      self.comboBox_node_type = QtGui.QComboBox(self.menu)
      self.comboBox_node_type.setGeometry(QtCore.QRect(10, 410, 221, 51))
      self.comboBox_node_type.setObjectName(_fromUtf8("comboBox_node_type"))
      self.comboBox_node_type.addItem(_fromUtf8(""))
      self.comboBox_node_type.addItem(_fromUtf8(""))
      self.comboBox_node_type.addItem(_fromUtf8(""))
      self.canvas = Canvas(self)
      self.canvas.setGeometry(QtCore.QRect(270, 10, 1221, 831))
      self.canvas.setObjectName(_fromUtf8("canvas"))
      
      self.label_eval = QtGui.QLabel(self.canvas)
      self.label_eval.setGeometry(QtCore.QRect(430, 10, 80, 40))
      self.label_eval.setObjectName(_fromUtf8("label_eval"))


      self.lineEdit_eval = QtGui.QLineEdit(self.canvas)
      self.lineEdit_eval.setGeometry(QtCore.QRect(550, 10, 100, 40))
      self.lineEdit_eval.setObjectName(_fromUtf8("lineEdit_eval"))

      self.pushButton_eval = QtGui.QPushButton("Evaluate",self.canvas)
      self.pushButton_eval.setGeometry(QtCore.QRect(680, 10, 100, 40))
      self.pushButton_eval.setObjectName(_fromUtf8("pushButton_eval"))

      self.comboBox_node_conv_type = QtGui.QComboBox(self.canvas)
      self.comboBox_node_conv_type.setGeometry(QtCore.QRect(800, 10, 100, 40))
      self.comboBox_node_conv_type.setObjectName(_fromUtf8("comboBox_node_type"))
      self.comboBox_node_conv_type.addItem("DFA")
      self.comboBox_node_conv_type.addItem("NFA")

      self.pushButton_conv = QtGui.QPushButton("Convert",self.canvas)
      self.pushButton_conv.setGeometry(QtCore.QRect(920, 10, 100, 40))
      self.pushButton_conv.setObjectName(_fromUtf8("pushButton_conv"))

      
      global canvas
      global mainWidget
      canvas     =  self.canvas
      mainWidget =  self

      self.retranslateUi()
      QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
      self.pushButton_edit.setText(_translate("MainWindow", "Editar", None))
      self.pushButton_delete.setText(_translate("MainWindow", "Borrar", None))
      self.pushButton_add.setText(_translate("MainWindow", "Agregar", None))
      self.comboBox_type.setItemText(0, _translate("MainWindow", "DFA", None))
      self.comboBox_type.setItemText(1, _translate("MainWindow", "NFA", None))
      self.comboBox_type.setItemText(2, _translate("MainWindow", "NFA EPSILON", None))
      self.label.setText(_translate("MainWindow", "Tipo", None))
      self.label_2.setText(_translate("MainWindow", "Valor", None))
      self.pushButton_save.setText(_translate("MainWindow", "Guardar", None))
      self.label_3.setText(_translate("MainWindow", " Nombre del Archivo", None))
      self.label_4.setText(_translate("MainWindow", "Menu", None))
      self.comboBox_node_type.setItemText(0, _translate("MainWindow", "START", None))
      self.comboBox_node_type.setItemText(1, _translate("MainWindow", "NORMAL", None))
      self.comboBox_node_type.setItemText(2, _translate("MainWindow", "FINAL", None))
      self.label_eval.setText(_translate("MainWindow", "EVALUATE", None))
      self.lineEdit_value.setText("Q0")
      self.eventManager() 


    def eventManager(self):
      self.DFA = 0;
      self.NFA = 1;
      self.NFA_E = 2;

      self.START = 0;
      self.NORMAL = 1;
      self.FINAL = 2;

      self.nodeTypeSelected = "NORMAL";
      self.fsmSelected = "DFA";

      self.canvas.mousePressEvent = self.mousePressEvent
      self.canvas.mousePressEvent = self.mousePressEvent
      self.setAcceptDrops(True)
      
      self.pushButton_add.clicked.connect(self.add)
      self.pushButton_edit.clicked.connect(self.edit)
      self.pushButton_delete.clicked.connect(self.delete)
      self.pushButton_save.clicked.connect(self.save)
      self.pushButton_load.clicked.connect(self.load)
      self.pushButton_eval.clicked.connect(evaluate)
      self.pushButton_conv.clicked.connect(convertNFAtoDFA)
      self.pushButton_deselect.clicked.connect(self.node_deselect)
      self.comboBox_type.currentIndexChanged.connect(self.changeType)
      self.comboBox_node_type.currentIndexChanged.connect(self.changeNodeType)


    def mousePressEvent(self, QMouseEvent):
      cursor = QtGui.QCursor()
      # print( QMouseEvent.pos())

    def mouseReleaseEvent(self, QMouseEvent):
      cursor = QtGui.QCursor()
      # print( cursor.pos()) 

    def save(self):
      print( "save")

    def load(self):
      print( "load")
      dlg = QtGui.QFileDialog()
      dlg.setFileMode(QtGui.QFileDialog.AnyFile)
      dlg.setFilter("Text files (*.*)")
      filenames = QtCore.QStringList()
      if dlg.exec_():
        filenames = dlg.selectedFiles()
        print( "Seleccionado ", filenames[0])

    def checkNodeExist(self, value):
      for node in nodeList:
        # print( "checking ", node.label.text(), " - ", value)
        if(node.label.text() == value):
          return True
      return False

    def checkConExist(self, node, value):
      for con in node.connections:
        # print( "checking ", con.name , " - ", value)
        if(con.name == value):
          return True
      return False

    def add(self):
      global startNode
      value = self.lineEdit_value.text() 
      if self.checkNodeExist(value):
        showMsg("Already Exist")
        print( "Exist")
      else:
        isFinal = False
        isStart = False
        nodeType = self.comboBox_node_type.currentText().lower()
        if(nodeType == "start"):
          isStart = True
          if startNode != None:
            showMsg("Already a start point")
            return
        elif(nodeType == "final"):
          print( "Final Node Created")
          isFinal = True
        else:
          print( "Normal Node Created")
        filename = nodeType+".png"
        new_node = Node(self.canvas, isStart, isFinal, filename, value )
        if(isStart):
          startNode = new_node
          print( "Start Node Created")
        print( "Node List: ", len(nodeList))
        mainWidget.lineEdit_value.setText("Q"+str(len(nodeList)))
      # print( "add ", new_label, filename)
      deselectGlobalNodes()

    def edit(self):
      global action
      action = "EDIT"
      print ("edit")
      value = mainWidget.lineEdit_value.text()
      option = mainWidget.comboBox_edit_type.currentText()
      print( "OPTION: ", option)
      if option == "NODE" :
        if currNode != None:
          if self.checkNodeExist(value):
            showMsg("Already Exist")
          else:
            currNode.label.setText(value)
      elif option == "CONNECTION":
        action = "EDIT_CON"
        index = self.comboBox_con.currentIndex() 
        print( "edit_con ", self.comboBox_con.currentText() , " index ", index)
        if( index != -1 ): 
          if currNode != None:
            if self.checkConExist(currNode, value):
              showMsg("Already Exist")
            else:
              currNode.connections[index].name = self.lineEdit_value.text()
      deselectGlobalNodes()

    def node_deselect(self):
      deselectGlobalNodes()

    def delete(self):
      global action
      option = mainWidget.comboBox_edit_type.currentText()
      print ("OPTION: ", option)
      if( option == "NODE" ):
        action = "DEL"
        if currNode != None:
          currNode.delNode()
        print( "delete")
      elif option == "CONNECTION":
        action = "DEL_CON"
        index = self.comboBox_con.currentIndex() 
        print( "Del_con ", self.comboBox_con.currentText() , " index ", index)
        if( index != -1 ): 
          conList[index].delCon(currNode)
      deselectGlobalNodes()

    def changeType(self, i):
      if i == self.DFA:
          typeName = 'DFA'
      elif i == self.NFA:
          typeName = 'NFA'
      elif i == self.NFA_E:
          typeName = 'NFA EPSILON'
      # print( "change: ", i, typeName ,self.comboBox_type.currentText())
      self.fsmSelected = typeName

    def changeNodeType(self, i):
      if i == self.START:
          typeName = 'START'
      elif i == self.NORMAL:
          typeName = 'NORMAL'
      elif i == self.FINAL:
          typeName = 'FINAL'
      # print( "change: ", i, typeName ,self.comboBox_node_type.currentText())
      self.fsmSelected = typeName

    def dragEnterEvent(self, e):
        e.accept()
        # print( "DRAG")

    def dropEvent(self, e):

        position = e.pos()        
        self.button.move(position)

        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
        # print( "DROP")

class Connection():
    def __init__(self, node, nextNode, same):
        self.node = node
        self.nextNode = nextNode
        self.same = same
        self.deleted = False
        self.name = mainWidget.lineEdit_value.text()
        self.red = randint(0, 255)
        self.green = randint(0, 255)
        self.blue = randint(0, 255)

    def delCon(self, node):
      self.deleted = True
      conList.remove(self)
      node.connections.remove(self);
      del self
      mainWidget.update()
      print( "Con List: ", len(conList))
        

class Node(QtGui.QLabel):
    def __init__(self, parent, first, final, img,name):
        QtGui.QLabel.__init__(self, parent)
        self.connections = []
        self.deleted = False
        self.setAcceptDrops(True)
        self.setPixmap(QtGui.QPixmap(_fromUtf8(img)))
        self.setScaledContents(True)
        self.setGeometry(QtCore.QRect(0, 0, 50, 50))
        self.move(50,50)
        self.show()

        self.selected = QtGui.QLabel(parent)
        self.selected.setScaledContents(True)
        self.selected.setPixmap(QtGui.QPixmap(_fromUtf8("select.png")))
        self.selected.setGeometry(QtCore.QRect(0, 0, 80, 80))
        self.selected.move(35,35)

        self.label = QtGui.QLabel(name, parent);
        self.label.move(45,100)
        self.label.show()
        
        nodeList.append(self)

        # self.pos       = pygame.mouse.get_pos()
        self.first     = first
        self.final     = final
        self.name      = name
        self.img       = img

    def moveNode(self, pos):
        self.move(pos)
        x = pos.x()
        y = pos.y()
        self.selected.move( x - 15, y -15 )
        self.label.move( x + 10 , y + 65 )

    def delNode(self):
      if(self.first):
        global startNode
        startNode = None
      self.deleted = True
      self.hide()
      self.label.hide()
      self.selected.hide()
      print( "Deleting from List ", nodeList.remove(self))
      del self.label
      del self.selected
      del self
      mainWidget.update()
      print ("Node List: ", len(nodeList))



    def showSelected(self):
        self.selected.show()
        self.raise_()

    def hideSelected(self):
        self.selected.hide()
        # print( "hide Select")

    def mousePressEvent(self, event):
        global action
        if(action == "EDIT"):
          print( "EDIT")
        if(action == "EDIT_CON"):
          print( "EDIT_CON")
        elif(action == 'DEL'):
          print ("DEL")
        else:
          self.__mousePressPos = None
          self.__mouseMovePos = None
          if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

          super(Node, self).mousePressEvent(event)
          selectGlobalNodes(self)
        action = ""
        

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            # print( 'DRAG')
            deselectGlobalNodes()
            self.moveNode(newPos)
            self.__mouseMovePos = globalPos
            mainWidget.repaint()
        super(Node, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        try:
          doSomething()
          if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return
            print( "DROP")
            mainWidget.repaint()
            mainWidget.update()
          super(Node, self).mouseReleaseEvent(event)
        except Exception: 
          print( "")
          # showMsg("ERROR")
        


def selectGlobalNodes(node):
  global currNode
  global nextNode

  if(currNode == None):
    currNode = node
    currNode.showSelected()
    for con in currNode.connections:
      mainWidget.comboBox_con.addItem(con.name)
    # print( 'First Node: ', currNode)
  else:
    nextNode = node
    connectNodes(node)
    deselectGlobalNodes()
    print( 'Second Label', nextNode)

def deselectGlobalNodes():
  global currNode
  global nextNode
  try:
    currNode.hideSelected()
    nextNode.hideSelected()
  except: 
    pass
    
  currNode = None
  nextNode = None
  mainWidget.comboBox_con.clear()
  mainWidget.canvas.repaint()
  mainWidget.canvas.update()

def connectNodes(nextNode):
  if(currNode != None and mainWidget.comboBox_edit_type.currentText() != "CONNECTION"):
    if(currNode == nextNode):
      isSame = True
    else:
      isSame = False
    if mainWidget.checkConExist(currNode, mainWidget.lineEdit_value.text()) and mainWidget.comboBox_type.currentText() == "DFA":
      showMsg("Already Exist")
    else:
      newCon = Connection(currNode, nextNode, isSame)
      currNode.connections.append(newCon)
      conList.append(newCon)
      mainWidget.update()
      print( "Conecting")


  else:
    print( "Seleccione un nodo")

def showMsg(text):
  msgBox = QtGui.QMessageBox( mainWidget )
  msgBox.setIcon( QtGui.QMessageBox.Information )
  msgBox.setText( text )

  # msgBox.setInformativeText( "Do you really want?" )
  # msgBox.addButton( QtGui.QMessageBox.No )
  msgBox.addButton( QtGui.QMessageBox.Yes )

  msgBox.setDefaultButton( QtGui.QMessageBox.Yes ) 
  ret = msgBox.exec_()

  # if ret == QtGui.QMessageBox.Yes:
  #     print( "Yes" )
  #     return
  # else:
  #     print( "No" )
  #     return

def is_final( name ):
    global Result
    for node in nodeList:
        if( node.label.text() == name ):
            if( node.final):
                Result = "Succesful, Last: "+name
                return True
    Result = "Failed, Last: "+name
    return False

def getStates():
  states = set()
  for node in nodeList:
    states.add(str(node.label.text()))
  # print("States ", str(states))
  return states

def getFinalStates():
  states = set()
  for node in nodeList:
    if(node.final):
      states.add(str(node.label.text()))
  print("final States ", str(states))
  return states

def getTransitions():
  keys = {}
  for node in nodeList:
    transitions = {}
    for con in node.connections:
      transitions[con.name] = str(con.nextNode.label.text())
    for k in symbols:
      try:
        print(k, ' - ', transitions[k] )
      except:
        transitions[k] = str(node.label.text())
    keys[str(node.label.text())] = transitions
  # print("Transitions ", str(keys))
  return keys

def getNFATransitions():
  keys = {}
  for node in nodeList:
    transitions = {}
    for con in node.connections:
      try:
        transitions[con.name].add( str(con.nextNode.label.text()) )
      except:
        transitions[con.name] = {str(con.nextNode.label.text())}
    for k in symbols:
      try:
        print(k, ' - ', transitions[k] )
      except:
        transitions[k] = {str(node.label.text())}
    keys[str(node.label.text())] = transitions
  print("Transitions ", str(keys))
  return keys


def get_events():
    events = []
    for con in conList:
        events.append( [ str(con.name) , str(con.node.label.text()) , str(con.nextNode.label.text()) ] )
        print( "appending con: ", str(con.name), "node: ", str(con.node.label.text()), "nextNode: ", str(con.nextNode.label.text()))
    return events

def evaluateDFA():
    print( "Eval DFA")
    # getStates()
    # getFinalStates()
    # getTransitions()
    value = str(mainWidget.lineEdit_eval.text())
    dfa = DFA(
      states= getStates(),
      input_symbols=symbols,
      transitions=getTransitions(),
      initial_state=str(startNode.label.text()),
      final_states=getFinalStates()
    )
    try:
      print(str(list(dfa.validate_input(value, step=True))))
      showMsg("DFA Successful, Last:" + str( dfa.validate_input(value) ) )
    except:
      showMsg("ERROR EVALUATING DFA")

    return dfa

def evaluateNFA():
    print( "Eval NFA")
    # NFA which matches strings beginning with 'a', ending with 'a', and containing
    # no consecutive 'b's
    value = str(mainWidget.lineEdit_eval.text())
    nfa = NFA(
        # states=getStates(),
        # input_symbols=symbols,
        # transitions={
        #     'q0': {'a': {'q1'}},
        #     # Use '' as the key name for empty string (lambda/epsilon) transitions
        #     'q1': {'a': {'q1'}, '': {'q2'}},
        #     'q2': {'b': {'q0'}}
        # },
        # initial_state='q0',
        # final_states={'q1'}
        states=getStates(),
        input_symbols=symbols,
        transitions=getNFATransitions(),
        initial_state=str(startNode.label.text()),
        final_states=getFinalStates()
    )
    try:
      listStates = list(nfa.validate_input(value, step=True))
      print(str( listStates ))
      showMsg("NFA Successful, Last:" + str( nfa.validate_input(value) ) )
    except:
      showMsg("ERROR EVALUATING NFA")

    return nfa

def searchNode(name):
  for node in nodeList:
    if(name == str(node.label.text()) ):
      return node
  return None

def convertNFAtoDFA():
  nfa = evaluateNFA()
  dfa = DFA(nfa)  # returns an equivalent DFA

  states      = dfa.states
  transitions = dfa.transitions
  initial     = dfa.initial_state
  finals       = dfa.final_states

  print( "states ",states, " transitions ", transitions, " initial ", initial, " final ", finals )

  global startNode
  global evalValue
  startNode = None
  evalValue = None

  currNode = None
  nextNode = None
  for node in nodeList:
    node.delNode()
  conList.clear()
  nodeList.clear()
  
  for state in states:
    isFinal = False
    isInitial = False
    img = "normal.png"
    if initial == state:
      isInitial = True
      img = "start.png"
    else:
      for f in finals:
        if f == state:
          isFinal = True
          img = "final.png"
    new_node = Node( mainWidget.canvas , isInitial, isFinal, img, state)
    nodeList.append(new_node)
    if(isInitial):
      startNode = new_node
      print("startNode ", new_node.label.text())

    #Py2
    #for key, value in d.iteritems():
    #Py3
  for key, value in transitions.items():
    n0 = searchNode(key)
    print("key ", key, " value ", str(value) )
    for key2, value2 in value.items():
      print("key2 ", key2, " value2 ", value2)
      isSameNode = False
      if(key == value2):
        isSameNode = True
      nX = searchNode(value2)
      # print(str(nX))
      new_connection = Connection( n0, nX, isSameNode)
      new_connection.name = key2
      conList.append(new_connection)

  # new_node = moveNode(self, pos)
  


def evaluate(): 
    global Result, evalValue
    evalValue = str(mainWidget.lineEdit_eval.text())
    fsmType = mainWidget.comboBox_type.currentText()
    print( "Evaluate ", evalValue)
    # if( startNode != None and evalValue != ""  ):
    #     events = get_events()
    #     try:
    #         fsm = Fysom(initial= str(startNode.label.text()) , events=events)
    #         for c in evalValue:
    #             fsm.trigger(c)
    #         print("Last State:", fsm.current, is_final(fsm.current)) #,
    #     except:
    #         print( "Something went wrong when evaluating")
    #         Result = "Failed"
    # else:
    #     Result =  "Failed"
    # showMsg(Result)

    if(fsmType == "DFA"):
      evaluateDFA()
    elif(fsmType == "NFA"):
      evaluateNFA()


if __name__ == '__main__':
  ui = Ui_MainWindow()
  ui.setupUi()
  ui.show()
  sys.exit(app.exec_())