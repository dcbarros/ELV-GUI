# -*- coding: utf-8 -*-

# Databank with this equation:
# Pvap[bar] = 10**(A - [B/(T[K]+C)])

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph.exporters
import shutil

import sys
import os
import numpy as np
import pandas as pd
import sqlite3

from thermo.unifac import UNIFAC
from thermo import Chemical

class Equilibrium(object):
    
    def __init__(self,lchem = None,p = None,t = None):
       
        self.lchem = lchem #Binary componets
        self.p = p #Pressure
        self.t = t #Temperature
        
    # Componets Data for the equilibrium
    def chemComp(self):
        
        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        cursor.execute('SELECT chemicals FROM AntoineConstant;')
        a = cursor.fetchall()
        listChemical = []
        for i in range(len(a)):
            listChemical.append(a[i][0])

        db.close()
        return listChemical

    def compData(self):
        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        self.A,self.B,self.C,self.Tmax,self.Tmin = np.zeros(len(self.lchem)),np.zeros(len(self.lchem)),np.zeros(len(self.lchem)),np.zeros(len(self.lchem)),np.zeros(len(self.lchem))

        self.DG= []
        '''
            1,2,3   - Antoine's Constant [Vapour Pressure is in bar]
            4,5     - Maximum and minimum Temperature for aplication this equation
            6       - List of Molecular Dortmund groups UNIFAC method
        '''

        for i in range(len(self.lchem)): 
            
            self.aux = [self.lchem[i]]
            cursor.execute('SELECT A,B,C,Tmin,Tmax FROM AntoineConstant WHERE chemicals =(?);',(self.aux))
            catch = cursor.fetchall()
            self.A[i],self.B[i],self.C[i],self.Tmax[i],self.Tmin[i] = catch[0][0],catch[0][1],catch[0][2],catch[0][3],catch[0][4]
            self.DG.append(Chemical(self.aux[0]).UNIFAC_Dortmund_groups)
        
        db.close()

        return self.A,self.B,self.C,self.Tmax,self.Tmin,self.DG

class Ui_Op2(object):

    def setupUi(self, Op2):

        listChem = Equilibrium()
        Op2.setObjectName("Op2")
        Op2.resize(950, 640)
        Op2.setMinimumSize(QtCore.QSize(950, 640))
        Op2.setMaximumSize(QtCore.QSize(950, 640))
        Op2.setWindowIcon(QtGui.QIcon('images\Icone.jpg'))
        Op2.setFocusPolicy(QtCore.Qt.NoFocus)
        Op2.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(Op2)
        self.centralwidget.setObjectName("centralwidget")
        
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, -1, 951, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 470, 961, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.graphicPlot = QtWidgets.QPushButton(self.centralwidget)
        self.graphicPlot.setGeometry(QtCore.QRect(480, 520, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)

        self.graphicPlot.setFont(font)
        self.graphicPlot.setObjectName("graphicPlot")

        self.graphics1 = PlotWidget(self.centralwidget)
        self.graphics1.setGeometry(QtCore.QRect(10, 10, 461, 401))
        self.graphics1.setBackground('w')
        self.graphics1.showGrid(x = True,y = True)
        self.graphics1.setObjectName("graphics1")

        self.graphics2 = PlotWidget(self.centralwidget)
        self.graphics2.setGeometry(QtCore.QRect(480, 10, 461, 401))
        self.graphics2.setBackground('w')
        self.graphics2.showGrid(x = True,y = True)
        self.graphics2.setObjectName("graphics2")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(310, 520, 171, 51))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.pconst = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.pconst.setEnabled(True)
        self.pconst.setCheckable(True)
        self.pconst.setChecked(False)
        self.pconst.setObjectName("pconst")
        self.verticalLayout_2.addWidget(self.pconst)

        self.tconst = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.tconst.setChecked(True)
        self.tconst.setObjectName("tconst")
        self.verticalLayout_2.addWidget(self.tconst)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(310, 490, 331, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.horizontalLayout.addItem(spacerItem)
        self.changeTextVar = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.changeTextVar.setFont(font)
        self.changeTextVar.setObjectName("changeTextVar")
        self.horizontalLayout.addWidget(self.changeTextVar)

        self.databox = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.databox.setFont(font)
        self.databox.setValidator(QtGui.QDoubleValidator())
        self.databox.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.databox.setToolTipDuration(1)
        self.databox.setObjectName("databox")

        self.horizontalLayout.addWidget(self.databox)
        self.changeTextUni = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.changeTextUni.setFont(font)
        self.changeTextUni.setObjectName("changeTextUni")

        self.horizontalLayout.addWidget(self.changeTextUni)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(260, 420, 431, 53))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)

        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.comp2 = QtWidgets.QComboBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        self.comp2.addItems(listChem.chemComp())
        font.setPointSize(9)
        self.comp2.setFont(font)
        self.comp2.setObjectName("comp2")
        self.gridLayout_2.addWidget(self.comp2, 1, 1, 1, 1)

        self.comp1 = QtWidgets.QComboBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        self.comp1.addItems(listChem.chemComp())
        font.setPointSize(9)
        self.comp1.setFont(font)
        self.comp1.setObjectName("comp1")
        self.gridLayout_2.addWidget(self.comp1, 1, 0, 1, 1)

        Op2.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Op2)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 950, 21))
        self.menubar.setObjectName("menubar")

        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")

        Op2.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Op2)
        self.statusbar.setObjectName("statusbar")
        Op2.setStatusBar(self.statusbar)

        self.actionsave2Excel = QtWidgets.QAction(Op2)
        self.actionsave2Excel.setObjectName("actionsave2Excel")

        #self.actionsavePlot = QtWidgets.QAction(Op2)
        #self.actionsavePlot.setObjectName("actionsavePlot")
        
        #self.addElement = QtWidgets.QAction(Op2)
        #self.addElement.setObjectName("addElement")

        self.about = QtWidgets.QAction(Op2)
        self.about.setObjectName("about")

        #self.removeElement = QtWidgets.QAction(Op2)
        #self.removeElement.setObjectName("removeElement")

        self.menuTools.addAction(self.actionsave2Excel)
        #self.menuTools.addAction(self.actionsavePlot)
        self.menuTools.addSeparator()
        #self.menuTools.addAction(self.addElement)
        #self.menuTools.addAction(self.removeElement)
        self.menuAbout.addAction(self.about)
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(Op2)
        QtCore.QMetaObject.connectSlotsByName(Op2)

        self.pconst.toggled.connect(lambda:self.selected(self.pconst))                                                      #Selection RadioButton Pressão Constante
        self.tconst.toggled.connect(lambda:self.selected(self.tconst))                                                      #Selection RadioButton Temperatura Constante                            
        self.graphicPlot.clicked.connect(lambda:self.call(float(self.databox.text()),self.changeTextUni.text()))            #Call the plot function
        self.actionsave2Excel.triggered.connect(lambda:self.saveData())
        self.about.triggered.connect(lambda:self.aboutMsg())

    def retranslateUi(self, Op2):
        _translate = QtCore.QCoreApplication.translate
        Op2.setWindowTitle(_translate("Op2", "Op_2 App"))
        self.graphicPlot.setText(_translate("Op2", "Plot"))
        self.pconst.setText(_translate("Op2", "Constant pressure "))
        self.tconst.setText(_translate("Op2", "Constant temperature "))
        self.changeTextVar.setText(_translate("Op2", "Temperature"))
        self.changeTextUni.setText(_translate("Op2", "K"))
        self.label_2.setText(_translate("Op2", "Substance 2"))
        self.label.setText(_translate("Op2", "Substance 1"))
        self.menuTools.setTitle(_translate("Op2", "Tools"))
        self.menuAbout.setTitle(_translate("Op2", "About"))
        self.actionsave2Excel.setText(_translate("Op2", "Save data to Excel"))
        #self.actionsavePlot.setText(_translate("Op2", "Salvar gráficos"))
        #self.addElement.setText(_translate("Op2", "Adicionar Elemento"))
        self.about.setText(_translate("Op2", "about"))
        #self.removeElement.setText(_translate("Op2", "Remover Elemento"))

    def selected(self,b):
        
        if b.text() == "Constant pressure ":
            if b.isChecked() == True:
                self.changeTextVar.setText('Pressure')
                self.changeTextUni.setText("bar")

        elif b.text() == "Constant temperature ":
            if b.isChecked() == True:
                self.changeTextVar.setText('Temperature')
                self.changeTextUni.setText("K")

    def call(self,data,signal,n = 1000):
        
        self.graphics1.clear(),self.graphics2.clear()
        x = np.arange(0,1.0+(1/n),(1/n))
        y,P,T = np.zeros(np.size(x)), np.zeros(np.size(x)), np.zeros(np.size(x))
        

        if signal == "bar":
            #Erase float_files
            if os.path.exists('float_files\\pconstdata.txt'):
                os.remove('float_files\\pconstdata.txt')
            try:
                data = open('float_files\\pconstdata.txt','a')
                newData = Equilibrium(lchem=[self.comp1.currentText(),self.comp2.currentText()],p = float(self.databox.text()))
                self.A,self.B,self.C,self.Tmax,self.Tmin,self.DG = newData.compData()
                Tsat = (self.B/(self.A-np.log10(float(self.databox.text()))))-self.C
                data.write('Temperature [K], x, y\n')
                for i in range(np.size(x)):
                    T0 = np.sum(np.asarray([x[i],1-x[i]])*Tsat)
                    while(True):
                        a12 = 10**(self.A[0] - self.A[1] -(self.B[0]/(T0+self.C[0])) + (self.B[1]/(T0+self.C[1])))
                        coef = UNIFAC(T = T0, xs = [x[i] , 1 - x[i]], chemgroups = self.DG)
                        P2sat = (float(self.databox.text())/(x[i]*coef[0]*a12+(1-x[i])*coef[1]))
                        Tn = (self.B[1]/(self.A[1] - np.log10(P2sat))) - self.C[1]
                        if (abs(Tn-T0)<0.001):
                            break
                        T0 = Tn
                    T[i] = T0
                    y[i] = 1 - ((1-x[i])*coef[1]*P2sat)/(float(self.databox.text()))
                    data.write(str(round(T[i],4))+', '+str(round(x[i],4))+', '+str(round(y[i],4)))
                    data.write('\n')

                self.graphics1.plot(x,y,pen = 'r')
                self.graphics1.plot(x,x,pen = 'r')
                self.graphics1.setLabel('left', 'Gas composition of ' + self.comp1.currentText(), color='r', size=20)
                self.graphics1.setLabel('bottom', 'Liquid composition of ' + self.comp1.currentText(), color='b', size=20)

                self.graphics2.plot(x,T,pen = 'g')
                self.graphics2.plot(y,T,pen = 'k')
                self.graphics2.setLabel('left', 'Temperature of ' + self.comp1.currentText() + ' [K]', color='r', size=20)
                self.graphics2.setLabel('bottom', 'Composition of ' + self.comp1.currentText(), color='b', size=20)
                
                data.close()
                

            except:
                print('error')

        elif signal == "K":
            #Erase float_files
            if os.path.exists('float_files\\tconstdata.txt'):
                os.remove('float_files\\tconstdata.txt')

            try:
                data = open('float_files\\tconstdata.txt','a')
                newData = Equilibrium(lchem=[self.comp1.currentText(),self.comp2.currentText()],t = float(self.databox.text()))
                self.A,self.B,self.C,self.Tmax,self.Tmin,self.DG = newData.compData()
                Pvap = 10**(self.A - (self.B/(float(self.databox.text())+self.C)))
                data.write('Pressure [bar], x, y\n')
                for i in range(np.size(x)):
                    actCoef = UNIFAC(T = float(self.databox.text()),xs = [x[i],1-x[i]],chemgroups = self.DG)
                    P[i] = np.sum(Pvap*np.asarray(actCoef)*np.asarray([x[i],1-x[i]]))
                    y[i] = ((x[i]*actCoef[0]*Pvap[0]))/P[i]
                    data.write(str(round(P[i],4))+', '+str(round(x[i],4))+', '+str(round(y[i],4)))
                    data.write('\n')

                self.graphics1.plot(x,y,pen = 'r')
                self.graphics1.plot(x,x,pen = 'r')
                self.graphics1.setLabel('left', 'Gas composition of ' + self.comp1.currentText(), color='r', size=20)
                self.graphics1.setLabel('bottom', 'Liquid composition of ' + self.comp1.currentText(), color='b', size=20)

                self.graphics2.plot(x,P,pen = 'b')
                self.graphics2.plot(y,P,pen = 'r')
                self.graphics2.setLabel('left', 'Pressure of ' + self.comp1.currentText() + ' [bar]', color='r', size=20)
                self.graphics2.setLabel('bottom', 'Composition of ' + self.comp1.currentText(), color='b', size=20)

                data.close()
                
            except:
                
                print('Error!')

    def saveData(self):
        
        if self.changeTextUni.text() == 'bar':
            try:
                filename = QtWidgets.QFileDialog.getSaveFileName(caption='Salvar arquivo',directory='c:\\',filter='(*.xlsx)',initialFilter='')
                data = pd.read_csv('float_files\\pconstdata.txt',sep = ', ')
                data.to_excel(excel_writer = filename[0])
                os.remove('float_files\\pconstdata.txt')
            except:
                pass

        elif self.changeTextUni.text() == 'K':
            try:
                filename = QtWidgets.QFileDialog.getSaveFileName(caption='Salvar arquivo',directory='c:\\',filter='(*.xlsx)',initialFilter='')
                data = pd.read_csv('float_files\\tconstdata.txt',sep = ', ')
                data.to_excel(excel_writer = filename[0])
                os.remove('float_files\\tconstdata.txt')
            except:
                pass
    
    def aboutMsg(self):
        
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('Sobre')
        msg.setWindowIcon(QtGui.QIcon('images\Icone.jpg'))
        msg.setText('Programa desenvolvido para calcular o equilíbrio de fase líquido-vapor de um sistema binário com fase vapor ideal e fase liquída não ideal cujo'+
        ' coeficiente de atividade é obtido por meio do método UNIFAC')
        x = msg.exec_()

if __name__ == "__main__":
    if os.path.exists('float_files\\pconstdata.txt') and os.path.exists('float_files\\tconstdata.txt'):
        
        os.remove('float_files\\pconstdata.txt')
        os.remove('float_files\\tconstdata.txt')

    app = QtWidgets.QApplication(sys.argv)
    Op2 = QtWidgets.QMainWindow()
    ui = Ui_Op2()
    ui.setupUi(Op2)
    Op2.show()
    sys.exit(app.exec_())
