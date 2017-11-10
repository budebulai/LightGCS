#/usr/bin/env python
# encoding:utf-8

from PyQt5.QtWidgets import QGraphicsView,\
                            QGraphicsScene,\
                            QGraphicsItem
from PyQt5.QtCore import QPointF
from PyQt5.QtSvg import QGraphicsSvgItem

"""
Attitude Director Indicator widget
"""
class flt_adi(QGraphicsView):
    def __init__(self, parent=None):
        super(flt_adi,self).__init__(parent)
        self.__paramsInit()

    def reinit(self):
        """
        reinitiate widget
        """
        self.__scene.clear()
        self.__init()

    def update(self):
        """
        redraws widget
        """
        self.__updateView()
        self.__faceDeltaXOld = self.__faceDeltaXNew
        self.__faceDeltaYOld = self.__faceDeltaYNew

    def setRoll(self, roll):
        """
        set roll angle, deg
        roll: float
        """
        self.__roll = roll

        if self.__roll < -180.0:
            self.__roll = -180.0
        elif self.__roll > 180.0:
            self.__roll = 180.0

    def setPitch(self, pitch):
        """
        set pitch angle, deg
        pitch: float
        """
        self.__pitch = pitch
        if self.__pitch < -25.0:
            self.__pitch = -25.0
        elif self.__pitch > 25.0:
            self.__pitch = 25.0

    def resizeEvent(self, event):
        QGraphicsView.resizeEvent(event)
        self.reinit()

    def __paramsInit(self):
        self.__roll = 0.0
        self.__pitch = 0.0

        self.__faceDeltaXNew = 0.0
        self.__faceDeltaXOld = 0.0
        self.__faceDeltaYNew = 0.0
        self.__faceDeltaYOld = 0.0

        self.__scaleX = 1.0
        self.__scaleY = 1.0

        self.__originalPixPerDeg = 1.7

        self.__originalHeight = 240
        self.__originalWidth = 240

        self.__backZ = -30
        self.__faceZ = -20
        self.__ringZ = -10
        self.__caseZ = 10

        self.__originalAdiCtr = QPointF(120.0,120.0)

        self.__scene = QGraphicsScene(self)
        self.__scene.clear()

    def __del__(self):
        self.__scene.clear()
        del self.__scene

        self.__reset()

    def __init(self):
        self.__scaleX = width() / self.__originalWidth
        self.__scaleY = height() / self.__originalHeight

        self.__reset()
        # "border-image: url(:/side_btn/LightGCS_image/setter.png);"
        self.__itemBack = QGraphicsSvgItem(":/fi_img/monitor/flightInstruments/img/adi/adi_back.svg")
        self.__itemBack.setCacheMode(QGraphicsItem.NoCache)
        self.__itemBack.setZvalue(self.__backZ)
        self.__itemBack.setTransform(QTransform.fromScale(self.__scaleX,self.__scaleY),True)
        self.__itemBack.setTransformOriginPoint(self.__originalAdiCtr)
        self.__scene.addItem(self.__itemBack)

        self.__itemFace = QGraphicsSvgItem(":/fi_img/monitor/flightInstruments/img/adi/adi_face.svg")
        self.__itemFace.setCacheMode(QGraphicsItem.NoCache)
        self.__itemFace.setZvalue(self.__faceZ)
        self.__itemFace.setTransform(QTransform.fromScale(self.__scaleX,self.__scaleY),True)
        self.__itemFace.setTransformOriginPoint(self.__originalAdiCtr)
        self.__scene.addItem(self.__itemFace)

        self.__itemRing = QGraphicsSvgItem(":/fi_img/monitor/flightInstruments/img/adi/adi_ring.svg")
        self.__itemRing.setCacheMode(QGraphicsItem.NoCache)
        self.__itemRing.setZvalue(self.__ringZ)
        self.__itemRing.setTransform(QTransform.fromScale(self.__scaleX,self.__scaleY),True)
        self.__itemRing.setTransformOriginPoint(self.__originalAdiCtr)
        self.__scene.addItem(self.__itemRing)

        self.__itemCase = QGraphicsSvgItem(":/fi_img/monitor/flightInstruments/img/adi/adi_case.svg")
        self.__itemCase.setCacheMode(QGraphicsItem.NoCache)
        self.__itemCase.setZvalue(self.__ringZ)
        self.__itemCase.setTransform(QTransform.fromScale(self.__scaleX,self.__scaleY),True)
        self.__itemCase.setTransformOriginPoint(self.__originalAdiCtr)
        self.__scene.addItem(self.__itemCase)

        centerOn(width()/2.0, height()/2.0)

        self.__updateView()

    def __reset(self):
        self.__roll = 0.0
        self.__pitch = 0.0

        self.__faceDeltaXNew = 0.0
        self.__faceDeltaXOld = 0.0
        self.__faceDeltaYNew = 0.0
        self.__faceDeltaYOld = 0.0

        del self.__itemBack
        del self.__itemFace
        del self.__itemRing
        del self.__itemCase

    def __updateView(self):
        self.__scaleX = width() / self.__originalWidth
        self.__scaleY = height() / self.__originalHeight

        self.__itemBack.setRotation(- self.__roll)
        self.__itemFace.setRotation(- self.__roll)
        self.__itemRing.setRotation(- self.__roll)

        roll_rad = math.PI * self.__roll / 180.0
        delta = self.__originalPixPerDeg * self.__pitch

        self.__faceDeltaXNew = self.__scaleX * delta * sin(roll_rad)
        self.__faceDeltaYNew = self.__scaleY * delta * cos(roll_rad)

        self.__itemFace.moveBy(self.__faceDeltaXNew - self.__faceDeltaXOld, self.__faceDeltaYNew - self.__faceDeltaYOld)
        self.__scene.update()
