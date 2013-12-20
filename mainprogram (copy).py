import sys
import os
import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import plots
import pyqtgraph as pg
jmetal_dir=str(os.getcwd()).split('/')
pfdir=jmetal_dir[:-1]
pfdir.append('pf')
pfdir='/'.join(pfdir)
print pfdir

#x = np.arange(10)
#y = np.arange(10) %3
#plt = pg.plot()
#plt.setWindowTitle('pyqtgraph example: ErrorBarItem')
#err = pg.ErrorBarItem(x=x, y=y, top=max(y)-y, bottom=y-min(y), beam=0)
#plt.addItem(err)
#plt.plot(x, y, pen={'color': 0.8, 'width': 2})



class mainDialog(QDialog,plots.Ui_plotdialog):
    def __init__(self,parent=None):
        super(mainDialog,self).__init__(parent)
        self.setupUi(self)
        firstoneht=self.readfirstone()
        files=os.listdir(pfdir)
        files=sorted(files)
        self.current_pf=files[0]
        for i in files:
            self.comboBox.addItem(i)
        w1=self.graphicsView.addPlot()
        s1=[]
        for solnum,val in firstoneht.items():

            x=range(1,len(val)+1)
            y=val
            print x
            print y
            s1.append(pg.ErrorBarItem(x=x, y=y, top=max(y)-y, bottom=y-min(y), beam=0))
        for x in s1:
            print x
            w1.addItem(x)
            break
        self.hslider.valueChanged.connect(self.plotgraph)
        self.comboBox.activated[str].connect(self.combo_chosen)

    def combo_chosen(self,value):
        print value
        self.current_pf=value
        with open(pfdir+'/'+self.current_pf,'r') as f:
            ptr=self.getxyvalues(f)
            self.s1.addPoints(pen='r',pos=ptr)


    def plotgraph(self,i):
        global jmetal_dir,pfdir
        #p1=self.graphicsView.plot()
        #p1.setPen((200,200,100))
        print i
        p=i/10+1
        #p=i+1
        #import numpy as np
        #x=np.random.random(10)
        #y=x*3
        #p=np.array(zip(x,y),dtype=[('x',float),('y',float)])
        #self.graphicsView.setData(p)
        self.s1.clear()
        dirctry=jmetal_dir[:-1]
        dirctry.append('abcGenerations')
        dirctry='/'.join(dirctry)
        self.hslider.setMaximum(10000)
        with open(dirctry+'/'+'generation'+str(p),'r') as f:
            ptr=self.getxyvalues(f)
            self.s1.addPoints(pos=ptr,pen=None)

        with open(pfdir+'/'+self.current_pf,'r') as f:
            ptr=self.getxyvalues(f)
            self.s1.addPoints(pen='r',pos=ptr)

    def getxyvalues(self,filepointer):
        t=filepointer.readline()
        val=[]
        while t:
            #print t
            val.append(tuple(map(lambda x:float(x),t.strip().split())))
            t=filepointer.readline()
        return val
    def readfirstone(self):
        global jmetal_dir,pfdir
        p=1
        dirctry=jmetal_dir[:-1]
        dirctry.append('abcGenerations')
        dirctry='/'.join(dirctry)
        self.hslider.setMaximum(10000)
        with open(dirctry+'/'+'generation'+str(p),'r') as f:
            ptr=self.getxyvalues(f)
            #self.s1.addPoints(pos=ptr,pen=None)
        dataframe=np.asarray(ptr)
        ht={}
        for i in range(len(dataframe[:,0])):
            ht[i]=dataframe[i,:]
        #print ht
        return ht

app = QApplication(sys.argv)
form = mainDialog()
form.show()
sys.exit(app.exec_())
