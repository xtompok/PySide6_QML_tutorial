from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel, QByteArray
from PySide2.QtGui import QGuiApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtPositioning import QGeoCoordinate
from PySide2 import QtCore
from enum import Enum
import typing
import sys
import json

VIEW_URL = "view.qml"
CITY_LIST_FILE = "souradnice.json"


class CityListModel(QAbstractListModel):
    class Roles(Enum):
        LOCATION = QtCore.Qt.UserRole+0
        AREA = QtCore.Qt.UserRole+1
        POPULATION = QtCore.Qt.UserRole+2

    def __init__(self,filename=None):
        QAbstractListModel.__init__(self)
        self.city_list = []
        if filename:
            self.load_from_json(filename)

    def load_from_json(self,filename):
        with open(filename,encoding="utf-8") as f:
            self.city_list = json.load(f)
            for c in self.city_list:
                pos = c['location']
                lon,lat = pos.split("(")[1].split(")")[0].split(" ")
                c['location'] = QGeoCoordinate(float(lat),float(lon))

    def rowCount(self, parent:QtCore.QModelIndex=...) -> int:
        return len(self.city_list)

    def data(self, index:QtCore.QModelIndex, role:int=...) -> typing.Any:
        print(index.row(),role)
        if role == QtCore.Qt.DisplayRole:
            return self.city_list[index.row()]["muniLabel"]
        elif role == self.Roles.LOCATION.value:
            #print(self.city_list[index.row()]["location"])
            return self.city_list[index.row()]["location"]
        elif role == self.Roles.AREA.value:
            return self.city_list[index.row()]["area"]
        elif role == self.Roles.POPULATION.value:
            return self.city_list[index.row()]["population"]

    def roleNames(self) -> typing.Dict:
        roles = super().roleNames()
        roles[self.Roles.LOCATION.value] = QByteArray(b'location')
        roles[self.Roles.AREA.value] = QByteArray(b'area')
        roles[self.Roles.POPULATION.value] = QByteArray(b'population')
        print(roles)
        return roles


app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
citylist_model = CityListModel(CITY_LIST_FILE)
ctxt = view.rootContext()
ctxt.setContextProperty('cityListModel',citylist_model)
view.setSource(url)
view.show()
app.exec_()
