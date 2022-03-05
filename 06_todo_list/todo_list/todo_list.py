from types import NoneType
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView
from PySide6 import QtCore
import typing
import sys
import json

VIEW_URL = "simple_view.qml"   # Simple user interface
#VIEW_URL = "view.qml"   # Advanced user interface
TASK_LIST_FILE = "ukoly.txt"


class TaskListModel(QAbstractListModel):
    """ Class for maintaining list of tasks"""

    def __init__(self,filename=None):
        """Initialize and load list from given file"""
        QAbstractListModel.__init__(self)
        self.task_list = []
        if filename:
            self.load_from_file(filename)

    def load_from_file(self,filename):
        """Load list of tasks from given file"""
        with open(filename,encoding="utf-8") as f:
            self.task_list =[l.strip() for l in f.readlines()]

    def rowCount(self, parent:QtCore.QModelIndex=...) -> int:
        """ Return number of cities in the list"""
        return len(self.task_list)

    def data(self, index:QtCore.QModelIndex, role:int=...) -> typing.Any:
        """ For given index and DisplayRole return the corresponding task"""
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            return self.task_list[index.row()]
	
    @Slot(str)
    def addTask(self,task: str) -> None:
        """ Add task to the end of the tasks list
        
        Arguments:
            - task - task to be added
        """
        self.beginInsertRows(self.index(0).parent(), self.rowCount(), self.rowCount())
        self.task_list.append(task)
        self.endInsertRows()

    @Slot(int)
    def deleteTask(self,idx: int) -> None:
        """ Delete task with given index from the list"""
        self.beginRemoveRows(self.index(0).parent(), idx, idx)
        self.task_list.pop(idx)
        self.endRemoveRows()

    @Slot(int)
    def clearTasks(self) -> None:
        """ Clear all tasks from the list"""
        self.beginRemoveRows(self.index(0).parent(), 0, self.rowCount()-1)
        self.task_list = []
        self.endRemoveRows()

app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
tasklist_model = TaskListModel(TASK_LIST_FILE)
ctxt = view.rootContext()
ctxt.setContextProperty('taskListModel',tasklist_model)
view.setSource(url)
view.show()
app.exec()
