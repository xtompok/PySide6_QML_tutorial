from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import  QQuickView
import sys

VIEW_PATH = "view.qml"

# Create the application object and pass command line arguments to it
app = QGuiApplication(sys.argv)

# Create the view object
view = QQuickView()
# Set the QML file to view
view.setSource(QUrl(VIEW_PATH))
# Resize the view with the window
view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
# Show the view (open the window)
view.show()

# Run the event loop
app.exec_()

