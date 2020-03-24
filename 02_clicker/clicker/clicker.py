from PySide2.QtCore import QObject, Slot, Property, QUrl, Signal
from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView

VIEW_URL = "view.qml"

class ClickModel(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._count = 0

    def get_count(self):
        return self._count

    def set_count(self,val):
        print("Have: {}, set: {}",self._count,val)
        if val != self._count:
            self._count = val
            self.notify_changed.emit()

    @Signal
    def notify_changed(self):
        print("Notifying")
        pass

    count = Property(int,get_count, set_count, notify=notify_changed)

    @Slot()
    def increase(self):
        print("Increasing")
        self.count = self.count+1

app = QApplication([])
view = QQuickView()
url = QUrl(VIEW_URL)
click_model = ClickModel()

ctxt = view.rootContext()
ctxt.setContextProperty("clickModel",click_model)

view.setSource(url)
view.show()
app.exec_()