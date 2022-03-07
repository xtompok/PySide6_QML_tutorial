import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.15

// Use ColumnLayout for resizable components
ColumnLayout {
	implicitWidth: 500	// width on the start of the program
	implicitHeight: 500	// height on the start of the program
	anchors.fill: parent

	Component {
		id: taskDelegate
		Item {
			width: parent.width 		// width as parent
			height: childrenRect.height	// height as CheckBox
			CheckBox {
				text: model.display	// only `display` clashes with CheckBox property
				checkable: true		// users can check
				onClicked: taskListModel.deleteTask(model.index)
			}
		}
	}

	
	ListView {
		Layout.fillWidth: true			// fill all available horizontal space in the window
		Layout.fillHeight: true			// fill all available vertical space in the window
		id: taskListView
		model: taskListModel
		delegate: taskDelegate
	}
	
	// Use RowLayout for resizable components 
	RowLayout {
		Layout.fillWidth: true			// this is property of the parent ColumnLayout
		Layout.alignment: Qt.AlignBottom	// this too, align the RowLayout to the bottom of the window

		// Border around TextInput for better visibility
		Rectangle {
			id: inputRect
			Layout.fillWidth: true
			Layout.alignment: Qt.AlignVCenter
			height: addTaskButton.height	// height is not implicitly inherited (width is), so use height from button
			border.width: 1
			border.color: "black"
			radius: 5

			TextInput {
				id: newTaskInput
				focus: true					// Take focus on start
				width: parent.width - 2				// Decrease the size because of the border
				height: parent.height - 2
				verticalAlignment: TextInput.AlignVCenter	// Align text vertically to the center of the component
				text: "Zadej další úkol"
				onAccepted: {					// When Enter is pressed 
					taskListModel.addTask(newTaskInput.text);	// Add task to the list
					newTaskInput.text = ""				// Clear the input text
				}
			}
		}
		Button {
			id: addTaskButton
			text: "Přidej úkol"
			onClicked: taskListModel.addTask(newTaskInput.text)
		}
		Button {
			text: "Odeber všechny úkoly"
			onClicked: taskListModel.clearTasks()
		}
	}
}