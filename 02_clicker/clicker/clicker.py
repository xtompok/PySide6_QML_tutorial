from PySide6.QtCore import QObject, Slot, Property, QUrl, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView
import sys

VIEW_URL = "view.qml"


class ClickModel(QObject):
    """ClickModel is the model class for the GUI. It holds the counter property
     and handles event generated by the click on the button."""
    def __init__(self):
        # Initialize the parent object. If omitted, GUI will not start
        QObject.__init__(self)
        # Initialize the counter internal value. Because we propagate count as
        # a property to QML, getter, setter and notifier must be made
        self._count = 0

    def get_count(self):
        """Getter for the count property"""
        return self._count

    def set_count(self,val):
        """Setter for the count property"""
        print("Current: {}, new: {}".format(self._count,val))
        # We set new value and notify of change only if the value
        # is really changed.
        if val != self._count:
            # Change internal value
            self._count = val
            # Notify the GUI that the value had changed
            self.counter_changed.emit()

    # Declare a notification method
    counter_changed = Signal()

    # Add a new property to ClickModel object. It can be used as an attribute
    # from Python.
    count = Property(int,get_count, set_count, notify=counter_changed)

    @Slot()
    def increase(self):
        """Handler for the button click. Increases counter by one."""
        print("Increasing")
        # Use property as an attribute. Setter is called automatically and
        # notifies the GUI about the changed value.
        self.count = self.count+1


app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
# Create the instance of a ClickModel
click_model = ClickModel()

# Get the context of the view
ctxt = view.rootContext()
# Set that 'click_model' will be available as 'clickModel' property in QML
# This must be done before view.setSource is called
ctxt.setContextProperty("clickModel",click_model)

view.setSource(url)
view.show()
app.exec_()
