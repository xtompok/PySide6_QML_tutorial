import QtQuick 2.14
import QtQuick.Controls 2.14


Column {
    id: column
    TextInput {
        id: remainingInput
        text: countdownModel.remaining
        width: parent.width

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
        anchors.centerIn: column.Center
        visible: false
        width: column.width
        height: column.height
        contentItem: Rectangle {

            color: "red"
            Text{
                anchors.centerIn: parent
                text:"Time out!"
            }
            MouseArea{
                anchors.fill: parent
                onClicked: {
                    timeoutPopup.close()
                }
            }
        }
        modal: true
        focus: true

    }
    Connections {
        target: countdownModel
        onTimeout: {timeoutPopup.visible = true }
    }


}
