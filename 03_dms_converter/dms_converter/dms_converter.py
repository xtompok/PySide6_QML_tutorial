from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView
import sys

VIEW_URL = "view.qml"

class DMSModel(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._deg = 0
        self._min = 0
        self._sec = 0
        self._deg_float = 0.0

    # Property 'deg'
    def set_deg(self, val):
        print(f"Current: {self._deg}, new: {val}")
        if val != self._deg:
            self._deg = val
            self.deg_changed.emit(self.deg)

    def get_deg(self):
        return self._deg

    deg_changed = Signal(int)
    deg = Property(int, get_deg, set_deg, notify=deg_changed)

    # Property 'min'
    def set_min(self, val):
        if val != self._min:
            self._min = val
            self.min_changed.emit(self._min)

    # Normal definition of function was shortened using lambda function
    get_min = lambda self: self._min
    min_changed = Signal(int)
    min = Property(int, get_min, set_min, notify=min_changed)

    def set_sec(self, val):
        if val != self._sec:
            self._sec = val
            self.sec_changed.emit(self._sec)

    sec_changed = Signal(int)
    # Getter lambda can be moved into the Property creation
    sec = Property(int, lambda self: self._sec, set_sec, notify=sec_changed)

    def set_deg_float(self, val):
        print(f"Current: {self._deg_float}, new: {val}")
        if val != self._deg_float:
            self._deg_float = val
            self.deg_float_changed.emit(self._deg_float)

    deg_float_changed = Signal(float)
    deg_float = Property(float, lambda self: self._deg_float, set_deg_float, notify=deg_float_changed)

    @Slot()
    def to_float(self):
        print("To float!")
        self.deg_float = self.deg + self.min/60 + self.sec/3600

    @Slot()
    def to_dms(self):
        print("To DMS!")
        val = float(self.deg_float)
        self.deg = int(val)
        val = (val-self.deg)*60
        self.min = int(val)
        val = (val-self.min)*60
        self.sec = int(val)


app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
dmsmodel = DMSModel()
ctxt = view.rootContext()
ctxt.setContextProperty('dmsmodel',dmsmodel)
view.setSource(url)
view.show()
app.exec_()
