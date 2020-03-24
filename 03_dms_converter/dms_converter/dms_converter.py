from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
import math

VIEW_URL = "view.qml"

class DMSModel(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._deg = 0
        self._min = 0
        self._sec = 0
        self._deg_float = 0.0

    def set_deg(self, val):
        print("Set deg? {}, {}",val,self._deg)
        if val != self._deg:
            print("Setting deg")
            self._deg = val
            self.deg_changed.emit()

    def get_deg(self):
        return self._deg

    @Signal
    def deg_changed(self):
        print("Deg changed!")
        pass

    deg = Property(int, get_deg, set_deg, notify=deg_changed)

    def set_min(self, val):
        if val != self._min:
            self._min = val
            self.min_changed.emit()

    def get_min(self):
        return self._min

    @Signal
    def min_changed(self):
        pass

    min = Property(int, get_min, set_min, notify=min_changed)

    def set_sec(self, val):
        if val != self._sec:
            self._sec = val
            self.sec_changed.emit()

    def get_sec(self):
        return self._sec

    @Signal
    def sec_changed(self):
        pass

    sec = Property(int, get_sec, set_sec, notify=sec_changed)

    def set_deg_float(self, val):
        if val != self._deg_float:
            self._deg_float = val
            self.deg_float_changed.emit()

    def get_deg_float(self):
        return self._deg_float

    @Signal
    def deg_float_changed(self):
        pass

    deg_float = Property(float, get_deg_float, set_deg_float, notify=deg_float_changed)

    @Slot()
    def to_float(self):
        print("To float!")
        self.deg_float = self.deg + self.min/60 + self.sec/3600

    @Slot()
    def to_dms(self):
        print("to DMS!")
        val = float(self.deg_float)
        self.deg = int(val)
        val = (val-self.deg)*60
        self.min = int(val)
        val = (val-self.min)*60
        self.sec = int(val)


app = QGuiApplication([])
engine = QQmlApplicationEngine()
dmsmodel = DMSModel()
ctxt = engine.rootContext()
ctxt.setContextProperty('dmsmodel',dmsmodel)
url = QUrl(VIEW_URL)
engine.load(url)


app.exec_()
