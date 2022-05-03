
import os
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
from PyQt5.QtWidgets import QFrame,QVBoxLayout,QFileDialog, QMainWindow,QApplication
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty
)
from vtkmodules.vtkRenderingVolume import vtkGPUVolumeRayCastMapper
from xml.dom.minidom import parse

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1140, 887)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Tapw = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Tapw.setFont(font)
        self.Tapw.setObjectName("Tapw")
        self.Rendering = QtWidgets.QWidget()
        self.Rendering.setObjectName("Rendering")
        self.VTK = QtWidgets.QWidget(self.Rendering)
        self.VTK.setGeometry(QtCore.QRect(0, 10, 931, 771))
        self.VTK.setObjectName("VTK")
        self.RenPreset = QtWidgets.QComboBox(self.Rendering)
        self.RenPreset.setGeometry(QtCore.QRect(950, 510, 161, 31))
        self.RenPreset.setObjectName("RenPreset")
        self.RenList = QtWidgets.QListWidget(self.Rendering)
        self.RenList.setGeometry(QtCore.QRect(950, 160, 161, 281))
        self.RenList.setObjectName("RenList")
        self.RenDelVolBtn = QtWidgets.QPushButton(self.Rendering)
        self.RenDelVolBtn.setGeometry(QtCore.QRect(940, 80, 171, 51))
        self.RenDelVolBtn.setObjectName("RenDelVolBtn")
        self.RenLoadVolBtn = QtWidgets.QPushButton(self.Rendering)
        self.RenLoadVolBtn.setGeometry(QtCore.QRect(940, 20, 171, 51))
        self.RenLoadVolBtn.setObjectName("RenLoadVolBtn")
        self.label_4 = QtWidgets.QLabel(self.Rendering)
        self.label_4.setGeometry(QtCore.QRect(990, 460, 101, 31))
        self.label_4.setObjectName("label_4")
        self.RenChange = QtWidgets.QPushButton(self.Rendering)
        self.RenChange.setGeometry(QtCore.QRect(940, 570, 171, 51))
        self.RenChange.setObjectName("RenChange")
        self.Tapw.addTab(self.Rendering, "")
        self.horizontalLayout.addWidget(self.Tapw)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1140, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.Tapw.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Volume Rendering"))
        self.RenDelVolBtn.setText(_translate("MainWindow", "Remove Volume"))
        self.RenLoadVolBtn.setText(_translate("MainWindow", "Add Volume"))
        self.label_4.setText(_translate("MainWindow", "Transfer Func"))
        self.RenChange.setText(_translate("MainWindow", "Change Transfer Func"))
        self.Tapw.setTabText(self.Tapw.indexOf(self.Rendering), _translate("MainWindow", "Volume Rendering"))


class VolumeRendering():
    def __init__(self,ui:Ui_MainWindow) -> None:
        self.frame = QFrame()
        self.ui = ui
        self.vl = QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
        self.ren = vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.colors = vtkNamedColors()
        self.vtkpros = {}
        self.colors.SetColor('BkgColor', [0, 0,0 , 255])
        self.ren.SetBackground(self.colors.GetColor3d('BkgColor'))
        self.frame.setLayout(self.vl)
        self.iren.Initialize()

        self.volumes = {}
        self.volume_property = vtkVolumeProperty()
        self.volume_color = vtkColorTransferFunction()
        self.volume_scalar_opacity = vtkPiecewiseFunction()
        self.volume_gradient_opacity = vtkPiecewiseFunction()
        self.setDefaultProperty()

        ui.RenLoadVolBtn.clicked.connect(partial(self.addVolumeBtn))
        ui.RenDelVolBtn.clicked.connect(partial(self.delVolumeBtn))
        ui.RenChange.clicked.connect(partial(self.changeBtn))
        self.readXML()
        self.volume_property = self.vtkpros["CT-AAA"]

    def readXML(self):
        # read preset property from preset.xml
        # the preset.xml is copied from 3D-Slicer
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        domtree = parse(os.path.join(cur_dir,"preset.xml"))
        data = domtree.documentElement
        propertys = data.getElementsByTagName('VolumeProperty')
        for pro in propertys:
            name = pro.getAttribute('name')
            go = pro.getAttribute('gradientOpacity')
            so = pro.getAttribute('scalarOpacity')
            ctrans = pro.getAttribute('colorTransfer')
            vtkpro = self.buildProperty(go,so,ctrans)
            self.vtkpros[name] = vtkpro
            self.ui.RenPreset.addItem(name)

    def buildProperty(self,go,so,ctrans):
        
        vtkcoltrans = vtkColorTransferFunction()
        data = ctrans.split()
        data = [float(x) for x in data]
        for i in range(int(data[0]/4)):
            base = 1 + i * 4
            # add 1000 because the intensity of our test data is started from 0
            # if you use the normal data, you can delete the const 1000.
            vtkcoltrans.AddRGBPoint(data[base] + 1000, data[base+1], data[base+2], data[base+3])

        vtkgo = vtkPiecewiseFunction()
        data = go.split()
        data = [float(x) for x in data]
        for i in range(int(data[0]/2)):
            base = 1 + i * 2
            vtkgo.AddPoint(data[base]+ 1000, data[base+1])

        vtkso = vtkPiecewiseFunction()
        data = so.split()
        data = [float(x) for x in data]
        for i in range(int(data[0]/2)):
            base = 1 + i * 2
            vtkso.AddPoint(data[base]+ 1000, data[base+1])

        vtkpro = vtkVolumeProperty()
        vtkpro.SetColor(vtkcoltrans)
        vtkpro.SetScalarOpacity(vtkso)
        #vtkpro.SetGradientOpacity(vtkgo)
        vtkpro.SetInterpolationTypeToLinear()
        vtkpro.ShadeOn()
        vtkpro.SetAmbient(0.4)
        vtkpro.SetDiffuse(0.6)
        vtkpro.SetSpecular(0.2)
        return vtkpro

    # add volume to the scene
    def addVolumeBtn(self):
        file_name,_ =QFileDialog.getOpenFileName(
            self.ui.Rendering,"open file dialog",os.getcwd(),"Mha(*.mha)")
        if file_name == "":
            return
        self.addVolume(file_name)
        self.ui.RenList.addItem(file_name)

    # delete volume from scene
    def delVolumeBtn(self):
        if not self.ui.RenList.itemAt(0,0):
            return
        curVol = self.ui.RenList.currentItem()
        if not curVol:
            curVol = self.ui.RenList.itemAt(0,0)
        curVol = curVol.text()
        self.delVolume(curVol)
        print(curVol)

    #change transfer function
    def changeBtn(self):
        curVol = self.ui.RenList.currentItem()
        if not curVol:
            curVol = self.ui.RenList.itemAt(0,0)
        curVol = curVol.text()
        if curVol in self.volumes.keys():
            self.volumes[curVol].SetProperty(self.vtkpros[self.ui.RenPreset.currentText()])

    def setDefaultProperty(self):
        self.volume_color.AddRGBPoint(0, 0.0, 0.0, 0.0)
        self.volume_color.AddRGBPoint(500, 240.0 / 255.0, 184.0 / 255.0, 160.0 / 255.0)
        self.volume_color.AddRGBPoint(1000, 240.0 / 255.0, 184.0 / 255.0, 160.0 / 255.0)
        self.volume_color.AddRGBPoint(1150, 1.0, 1.0, 240.0 / 255.0)  # Ivory

        self.volume_scalar_opacity = vtkPiecewiseFunction()
        self.volume_scalar_opacity.AddPoint(0, 0.00)
        self.volume_scalar_opacity.AddPoint(500, 0.15)
        self.volume_scalar_opacity.AddPoint(1000, 0.15)
        self.volume_scalar_opacity.AddPoint(1150, 0.85)

        self.volume_gradient_opacity = vtkPiecewiseFunction()
        self.volume_gradient_opacity.AddPoint(0, 0.0)
        self.volume_gradient_opacity.AddPoint(90, 0.5)
        self.volume_gradient_opacity.AddPoint(100, 1.0)
        self.volume_property = vtkVolumeProperty()
        self.volume_property.SetColor(self.volume_color)
        self.volume_property.SetScalarOpacity(self.volume_scalar_opacity)
        self.volume_property.SetGradientOpacity(self.volume_gradient_opacity)
        self.volume_property.SetInterpolationTypeToLinear()
        self.volume_property.ShadeOn()
        self.volume_property.SetAmbient(0.4)
        self.volume_property.SetDiffuse(0.6)
        self.volume_property.SetSpecular(0.2)

    def delVolume(self,path):
        self.ren.RemoveViewProp(self.volumes[path])
        item = self.ui.RenList.findItems(path,QtCore.Qt.MatchExactly)[0]
        row = self.ui.RenList.row(item)
        self.ui.RenList.takeItem(row)
        self.volumes.pop(path)
        self.iren.Initialize()

    def addVolume(self,path):
        reader = vtkMetaImageReader()
        reader.SetFileName(path)
        volume_mapper = vtkGPUVolumeRayCastMapper()
        volume_mapper.SetInputConnection(reader.GetOutputPort())
        volume = vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(self.volume_property)

        self.ren.AddViewProp(volume)
        self.volumes[path] = volume
        camera = self.ren.GetActiveCamera()
        c = volume.GetCenter()
        camera.SetViewUp(0, 0, -1)
        camera.SetPosition(c[0], c[1] - 800, c[2]-200)
        camera.SetFocalPoint(c[0], c[1], c[2])
        camera.Azimuth(30.0)
        camera.Elevation(30.0)
        self.iren.Initialize()
       
    
def main():
    app = QApplication([])
    mainw =  QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainw)
    mvtk = VolumeRendering(ui)
    mvtk.frame.setGeometry(0,0,1000,1000)
    mvtk.frame.setParent(ui.VTK)
    mainw.show()
    app.exec_()


if __name__ == "__main__":
    main()