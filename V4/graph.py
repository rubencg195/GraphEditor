import sys
import json
from random import randint
from PyQt4 import QtCore, QtGui

from fysom import Fysom
# from automata.fa.dfa import DFA
# from automata.fa.nfa import NFA

import logging
import pickle 
import re

from DFA   import DFA
from NFA   import NFA
from NFA_e import NFAe

from grammaregex import print_tree, match_tree, find_tokens, verify_pattern, PatternSyntaxException
import AutomataLib

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
alphabet = "0,1"
# alphabet = "0,1,2,3,4,5,6,7"
# testFilename = "/home/ruben/Desktop/Computer Theory/V3/examples/DFA"
testFilename = "/home/ruben/Desktop/Computer Theory/V3/examples/cantidad 1 y 0 impar V3"
# testFilename = "/home/ruben/Desktop/Computer Theory/V3/examples/NFA_e"

logger = logging.Logger('catch_all')
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

class Canvas(QtGui.QWidget):
    def __init__(self, parent):
      QtGui.QWidget.__init__(self, parent)

    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        for con in conList:
          try:
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

      self.lineEdit_eval = QtGui.QLineEdit(self.canvas)
      self.lineEdit_eval.setGeometry(QtCore.QRect(300, 10, 100, 40))
      self.lineEdit_eval.setObjectName(_fromUtf8("lineEdit_eval"))

      self.label_eval = QtGui.QLabel(self.canvas)
      self.label_eval.setGeometry(QtCore.QRect(200, 10, 80, 40))
      self.label_eval.setObjectName(_fromUtf8("label_eval"))

      self.pushButton_eval = QtGui.QPushButton("Evaluate",self.canvas)
      self.pushButton_eval.setGeometry(QtCore.QRect(750, 10, 100, 40))
      self.pushButton_eval.setObjectName(_fromUtf8("pushButton_eval"))

      self.label_regex = QtGui.QLabel("REGEX", self.canvas)
      self.label_regex.setGeometry(QtCore.QRect(450, 10, 100, 40))
      self.label_regex.setObjectName(_fromUtf8("label_regex"))

      self.lineEdit_regex = QtGui.QLineEdit("(0|(1(01*(00)*0)*1)*)*",self.canvas)
      self.lineEdit_regex.setGeometry(QtCore.QRect(500, 10, 200, 40))
      self.lineEdit_regex.setObjectName(_fromUtf8("lineEdit_regex"))

      self.pushButton_conv = QtGui.QPushButton("Convert",self.canvas)
      self.pushButton_conv.setGeometry(QtCore.QRect(850, 10, 100, 40))
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
      self.comboBox_type.setItemText(3, _translate("MainWindow", "REGEX", None))
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
      self.pushButton_conv.clicked.connect(convert)
      self.pushButton_deselect.clicked.connect(self.node_deselect)
      self.comboBox_type.currentIndexChanged.connect(self.changeType)
      self.comboBox_node_type.currentIndexChanged.connect(self.changeNodeType)
 
    def mousePressEvent(self, QMouseEvent):
      cursor = QtGui.QCursor()
    def mouseReleaseEvent(self, QMouseEvent):
      cursor = QtGui.QCursor()

    def save(self):
      print( "save")
      dlg = QtGui.QFileDialog()
      dlg.setFileMode(QtGui.QFileDialog.AnyFile)
      if dlg.exec_():
        filenames = dlg.selectedFiles()
        print( "Seleccionado ", filenames[0])
        filehandler = open(filenames[0], 'wb') 

        saveNodeList = []
        saveConList  = []
        for node in nodeList:  
          saveNodeList.append( { "first": node.first , "final": node.final , "img": node.img , "name": str(node.label.text()), "x":node.x(), "y":node.y() } )
        pickle.dump( saveNodeList , filehandler) 

        for con in conList:
          saveConList.append( { "name":con.name , "same":con.same , "node": str(con.node.label.text()) , "nextNode":str(con.nextNode.label.text()) } )
        pickle.dump( saveConList , filehandler)

        pickle.dump( alphabet , filehandler) 
        pickle.dump( self.lineEdit_eval.text() , filehandler)
        pickle.dump( symbols , filehandler)


    def load(self, test = False):
      print( "load")
      global startNode
      global evalValue
      global nodeList
      global conList
      global symbols

      for con in conList:
        try:
          con.node.delNode()
        except:
          print("err del node from con")
        try:
          con.nextNode.delNode()
        except:
          print("err del nextNode from con")
      for node in nodeList:
         try:
          node.delNode()
         except:
          print("err del node from nodeList")        

      dlg = QtGui.QFileDialog()
      dlg.setFileMode(QtGui.QFileDialog.AnyFile)
      # dlg.setFilter("Text files (*.*)")

      filenames = []
      windowOpened = False
      if not test:
          windowOpened = dlg.exec_()
          filenames = dlg.selectedFiles()
      else:
          filenames = [testFilename]
      

      if windowOpened or  test:         
        filehandler = open(filenames[0], 'rb') 
        
        loadNodeList = pickle.load( filehandler )
        conNodeList  = pickle.load( filehandler )

        for n in loadNodeList :
          new_node = Node(self.canvas, n["first"], n["final"], n["img"], n["name"] )
          new_node.moveNode(QtCore.QPoint(n['x'], n['y']))
          if n["first"]:
            startNode = new_node

        for c in conNodeList  :
          conNode     = findNode( c["node"] )
          conNextNode = findNode( c["nextNode"])
          newCon = Connection(conNode , conNextNode , c["same"] ) 
          newCon.name = c["name"]
          conNode.connections.append(newCon)
          conList.append(newCon)

        alphabet  = pickle.load(filehandler) 
        evalValue = pickle.load(filehandler)
        symbols   = pickle.load( filehandler)
        self.lineEdit_eval.setText(evalValue)

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
      # self.fsmSelected = typeName

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
      mainWidget.update()
      del self
      print( "Con List: ", len(conList))
        
class Node(QtGui.QLabel):
    def __init__(self, parent, first, final, img,name):
        QtGui.QLabel.__init__(self, parent)
        super(Node, self).__init__(parent=parent)
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
      self.deleted = True
      self.label.hide()
      self.selected.hide()
      self.hide()
      mainWidget.update()

      if(self.first):
        global startNode
        startNode = None
      
      print( "Deleting from List ", nodeList.remove(self))
      del self.label
      del self.selected
      del self
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

def findNode(name):
  for n in nodeList:
    if str(n.label.text()) == name:
      return n
  return None

def get_events():
    events = []
    for con in conList:
        events.append( [ str(con.name) , str(con.node.label.text()) , str(con.nextNode.label.text()) ] )
        print( str(con.node.label.text()), " --", str(con.name), "--> ", str(con.nextNode.label.text()))
    return events

def get_transitions():
  keys = {}
  for node in nodeList:
    transitions = {}
    for con in node.connections:
      transitions[con.name] = str(con.nextNode.label.text())
    for k in symbols:
      try:
        # print(k, ' - ', transitions[k] )
        pass
      except:
        transitions[k] = str(node.label.text())
    keys[str(node.label.text())] = transitions
  return keys

def createDFA():
  newDFA = DFA("newDFA", alphabet)
  print("nodes addState")
  for node in nodeList:
    newDFA.addState( str(node.label.text()), node.first, node.final )
  for con in conList:
    newDFA.addTransition( str(con.name), str(con.node.label.text()),  str(con.nextNode.label.text()) )
  return newDFA

def createNFA():
  newNFA = NFA("newNFA", alphabet)
  print("nodes addState")
  for node in nodeList:
    newNFA.addState( str(node.label.text()), node.first, node.final )
  for con in conList:
    newNFA.addTransition( str(con.name), str(con.node.label.text()),  str(con.nextNode.label.text()) )
  return newNFA

def createNFAe():
  newNFAe = NFAe("newNFAe", alphabet)
  print("nodes addState")
  for node in nodeList:
    newNFAe.addState( str(node.label.text()), node.first, node.final )
  for con in conList:
    newNFAe.addTransition( str(con.name), str(con.node.label.text()),  str(con.nextNode.label.text()) )
  return newNFAe

def evaluateREGEX():
  regex = str( mainWidget.lineEdit_regex.text() )
  pattern = re.compile( regex )
  print("REGEX ", pattern.match( evalValue ) )

  if bool(re.match( regex , evalValue )):
    msg = evalValue+" succesfully pass "+regex
  else:
    msg = evalValue+" failed "+regex
  showMsg(msg)

def evaluate():
  print("Events "+mainWidget.comboBox_type.currentText() )
  get_events()
  evalValue = str(mainWidget.lineEdit_eval.text())
  automata = None
  if   mainWidget.comboBox_type.currentText() == "DFA":
    automata = createDFA()
  elif mainWidget.comboBox_type.currentText() == "NFA":
    automata = createNFA()
  elif mainWidget.comboBox_type.currentText() == "NFA EPSILON":
    automata = createNFAe()
  elif mainWidget.comboBox_type.currentText() == "REGEX":
    evaluateREGEX()
    return
  msg = "Evaluating " + evalValue + " last state " + automata.match( evalValue ).label 
  showMsg(msg)

def convert():
  print("CONVERT "+mainWidget.comboBox_type.currentText() )
  get_events()
  evalValue = str(mainWidget.lineEdit_eval.text())
  if   mainWidget.comboBox_type.currentText() == "DFA":
    DFAtoREGEX()
  elif mainWidget.comboBox_type.currentText() == "NFA":
    NFAtoDFA()
  elif mainWidget.comboBox_type.currentText() == "NFA EPSILON":
    NFAetoDFA()
  elif mainWidget.comboBox_type.currentText() == "REGEX":
    REGEXtoNFAe()

def NFAtoDFA():
  print("convert NFA to DFA")
  automata = createNFA()
  newDFA = automata.toDFA()
  regenerateAutomata(newDFA)
  mainWidget.comboBox_type.setCurrentIndex(0)

def NFAetoDFA():
  print("convert NFAe to DFA")
  automata = createNFAe()
  newDFA = automata.toDFA()
  regenerateAutomata(newDFA)
  mainWidget.comboBox_type.setCurrentIndex(0)

def DFAtoREGEX():
  print("DFA to REGEX")
  automata = createDFA()
  toRE =  automata.toRE()
  # print("toRE ", toRE['regex'], " - ", toRE["stepByStep"] )
  showMsg("DFA to RE: "+ toRE['regex'])
  mainWidget.lineEdit_regex.setText(toRE['regex'])
  mainWidget.comboBox_type.setCurrentIndex(3)

def REGEXtoNFAe():
  print("REGEX to NFAe")
  nfaLib = AutomataLib.RegExp( str(mainWidget.lineEdit_regex.text() ) )
  print( "NFA ", nfaLib )

  newNFA = NFAe("newNFA", alphabet)
  for s in nfaLib.states() :
    print("state ", s)
    newNFA.addState( "Q"+str(s), s in nfaLib.initial, nfaLib.isfinal(s) )
  # for con in conList:
  #   newNFA.addTransition( str(con.name), str(con.node.label.text()),  str(con.nextNode.label.text()) )
  for s in nfaLib.states() :
    for c in nfaLib.alphabet:
      for neighbor in nfaLib.transition(s,c):
          if str(c) == '|':
            c = 'E'
          print( s ,"  --[" + str(c) + "]-->", neighbor )
          newNFA.addTransition(str(c) , "Q"+str(s), "Q"+str(neighbor) )

  regenerateAutomata(newNFA)
  mainWidget.comboBox_type.setCurrentIndex(2)
  
def regenerateAutomata(automata):
  print( "Regenerate")
  global startNode
  global evalValue
  global nodeList
  global conList
  global symbols
  emptyLists()
    
  for s in automata.states:
    img = "normal.png"
    if s.isInitial:
      img = "start.png"
    elif s.isFinal:
      img = "final.png"

    randomX = randint(30, 800) 
    randomY = randint(30, 600)

    new_node = Node(canvas, s.isInitial , s.isFinal , img, s.label )
    new_node.moveNode(QtCore.QPoint( randomX , randomY ))
    if s.isInitial:
      startNode = new_node

  for s in automata.states:
    for t in s.transitions:
      conNode     = findNode( t._from )
      conNextNode = findNode( t._to   )
      newCon = Connection(conNode , conNextNode , t._from == t._to  ) 
      newCon.name = t.label
      conNode.connections.append(newCon)
      conList.append(newCon)


def emptyLists():
  for con in conList:
    try:
      con.node.delNode()
    except:
      print("err del node from con")
    try:
      con.nextNode.delNode()
    except:
      print("err del nextNode from con")
  for node in nodeList:
     try:
      node.delNode()
     except:
      print("err del node from nodeList")     

if __name__ == '__main__':
  ui = Ui_MainWindow()
  ui.setupUi()
  ui.show()
  ui.load(True)
  sys.exit(app.exec_())