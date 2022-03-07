import QtQuick 2.14
import QtQuick.Controls 2.14

Column {
	width: 500
	height: 500

	Component {
		id: taskDelegate
		Item {
			width: parent.width
			height: childrenRect.height

			Text {text: display}
			MouseArea {
				anchors.fill: parent
				onClicked: taskListView.currentIndex = index
			}
		}
	}

	ListView {
		id: taskListView
		width: parent.width
		height: 300
		model: taskListModel
		delegate: taskDelegate
		highlight: Rectangle {
			color: "red"
		}
	}

	TextInput {
		id: newTaskInput
		text: "Zadej další úkol"
	}
	Button {
		text: "Přidej úkol"
		// Send signal with one argument - text written in newTaskInput
		onClicked: taskListModel.addTask(newTaskInput.text)
	}
	Button {
		text: "Odeber zvolený úkol"
		// Send signal with one argument - index of the currently selected item
		onClicked: taskListModel.deleteTask(taskListView.currentIndex)
	}
}