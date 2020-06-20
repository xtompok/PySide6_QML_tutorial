from PySide2.QtCore import QObject, Slot, Property, QUrl, Signal, QTimer, QAbstractListModel, QByteArray
from PySide2.QtGui import QGuiApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide2.QtPositioning import QGeoCoordinate
from PySide2 import QtCore
from dataclasses import dataclass
import sys
from enum import Enum
import json
import typing

VIEW_URL = "view.qml"
POSITIONS_URL = "https://mapa.idsjmk.cz/api/vehicles.json"
UPDATE_INTERVAL = 5000 # ms

@dataclass
class Vehicle(object):
    pos : QGeoCoordinate
    id : int

class VehiclesModel(QAbstractListModel):

    class Roles(Enum):
        LOCATION = QtCore.Qt.UserRole+0
        ID = QtCore.Qt.UserRole+1

        def __repr__(self):
            return "V({})".format(self.id)

    def __init__(self,na_manager: QNetworkAccessManager):
        QAbstractListModel.__init__(self)
        self.vehicle_list = []
        self.na_manager = na_manager
        self.na_manager.finished[QNetworkReply].connect(self.download_finished)
        self.timer = QTimer()
        self.timer.setInterval(UPDATE_INTERVAL)
        self.timer.timeout.connect(self.start_download)
        self.timer.start()

    def rowCount(self, parent:QtCore.QModelIndex=...) -> int:
        return len(self.vehicle_list)

    def data(self, index:QtCore.QModelIndex, role:int=...) -> typing.Any:
        print(index.row(),role)
        if role == QtCore.Qt.DisplayRole:
            return self.vehicle_list[index.row()].id

        if role == self.Roles.ID.value:
            return self.vehicle_list[index.row()].id

        if role == self.Roles.LOCATION.value:
            print("Position:",self.vehicle_list[index.row()].pos)
            return self.vehicle_list[index.row()].pos

    def roleNames(self) -> typing.Dict:
        """Returns dict with role numbers and role names for default and custom roles together"""
        # Append custom roles to the default roles and give them names for a usage in the QML
        roles = super().roleNames()
        roles[self.Roles.LOCATION.value] = QByteArray(b'location')
        roles[self.Roles.ID.value] = QByteArray(b'id')
        print(roles)
        return roles

    @Slot()
    def start_download(self):
        print("Downlad started")
        self.na_manager.get(QNetworkRequest(QUrl(POSITIONS_URL)))

    @Slot()
    def download_finished(self,reply:QNetworkReply):
        print("Download finished")
        reply_str = reply.readAll().data()
        print(type(reply_str))
        reply_str = reply_str.decode('utf-8-sig')
        data = json.loads(reply_str)
        print(data)
        self.update_data(data)

    def update_data(self,data):
        vehicles = data['Vehicles']
        self.beginRemoveRows(self.index(0).parent(),0,len(self.vehicle_list)-1)
        self.vehicle_list = []
        self.endRemoveRows()
        self.beginInsertRows(self.index(0).parent(),0,len(vehicles)-1)
        for v in vehicles:
            pos = QGeoCoordinate(float(v['Lat']),float(v['Lng']))
            aid = v['ID']
            self.vehicle_list.append(Vehicle(pos,aid))
        self.endInsertRows()
        print(self.vehicle_list)





app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
na_manager = QNetworkAccessManager()
vehicles_model = VehiclesModel(na_manager)

ctxt = view.rootContext()
ctxt.setContextProperty("vehiclesModel", vehicles_model)

view.setSource(url)
view.show()
app.exec_()
