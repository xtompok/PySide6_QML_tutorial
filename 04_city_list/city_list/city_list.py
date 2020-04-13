from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel
from PySide2.QtGui import QGuiApplication
from PySide2.QtQuick import QQuickView
from PySide2 import QtCore
import typing
import sys
import json

#VIEW_URL = "simple_view.qml"
VIEW_URL = "view.qml"
CITY_LIST_FILE = "souradnice.json"


class CityListModel(QAbstractListModel):
    def __init__(self,filename=None):
        QAbstractListModel.__init__(self)
        self.city_list = []
        if filename:
            self.load_from_json(filename)

    def load_from_json(self,filename):
        with open(filename,encoding="utf-8") as f:
            self.city_list = json.load(f)

    def rowCount(self, parent:QtCore.QModelIndex=...) -> int:
        return len(self.city_list)

    def data(self, index:QtCore.QModelIndex, role:int=...) -> typing.Any:
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
