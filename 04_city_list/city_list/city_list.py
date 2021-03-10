from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView
from PySide6 import QtCore
import typing
import sys
import json

#VIEW_URL = "simple_view.qml"   # Simple user interface
VIEW_URL = "view.qml"   # Advanced user interface
CITY_LIST_FILE = "souradnice.json"


class CityListModel(QAbstractListModel):
    """ Class for maintaining list of cities"""

    def __init__(self,filename=None):
        """Initialize and load list from given file"""
        QAbstractListModel.__init__(self)
        self.city_list = []
        if filename:
            self.load_from_json(filename)

    def load_from_json(self,filename):
        """Load list of cities from given file"""
        with open(filename,encoding="utf-8") as f:
            self.city_list = json.load(f)

    def rowCount(self, parent:QtCore.QModelIndex=...) -> int:
        """ Return number of cities in the list"""
        return len(self.city_list)

    def data(self, index:QtCore.QModelIndex, role:int=...) -> typing.Any:
        """ For given index and DisplayRole return name of the selected city"""
        # Return None if the index is not valid
        if not index.isValid():
            return None
        # If the role is the DisplayRole, return name of the city
        if role == QtCore.Qt.DisplayRole:
            return self.city_list[index.row()]["muniLabel"]


app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
citylist_model = CityListModel(CITY_LIST_FILE)
ctxt = view.rootContext()
ctxt.setContextProperty('cityListModel',citylist_model)
view.setSource(url)
view.show()
app.exec_()
