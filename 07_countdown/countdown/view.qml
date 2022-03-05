import QtQuick 2.14
import QtQuick.Controls 2.14


Column {
    id: column
    TextInput {
        id: remainingInput
        text: countdownModel.remaining
        width: parent.width
        // Align text to the horizontal center of the column
        horizontalAlignment: TextInput.AlignHCenter

        // Update a property if the number is changed in the TextInput
        Binding {
                target: countdownModel
                property: "remaining"
                value: remainingInput.text
            }
    }
    Button {
        text: 'Start'
        onClicked: countdownModel.start()
    }
    Button {
        text: 'Pause'
        onClicked: countdownModel.pause()
    }
    Button {
        text: 'Stop'
        onClicked: countdownModel.stop()
    }

    Popup{
        id: timeoutPopup
        // Exactly overlay the parent window
        anchors.centerIn: column.Center
        width: column.width
        height: column.height

        visible: false
        contentItem: Rectangle {

            color: "red"
            Text{
                anchors.centerIn: parent
                text:"Time out!"
            }
            MouseArea{
                anchors.fill: parent
                onClicked: {
                    // Close the popup if there was clicked anywhere on it
                    timeoutPopup.close()
                }
            }
        }

        // Popup is modal and wants focus
        modal: true
        focus: true
    }

    // Show the popup on timeout signal emitted
    Connections {
        target: countdownModel
        onTimeout: {timeoutPopup.visible = true }
    }


}
