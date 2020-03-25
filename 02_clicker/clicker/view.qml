import QtQuick 2.14
import QtQuick.Controls 2.14


Column {
    Text {
        // Bind the clickModel.count property to the text property of the QML element
        text: clickModel.count
    }
    Button {
        text: 'Click me!'
        // Connect the clickModel.increase slot to the onClicked signal
        onClicked: clickModel.increase()
    }
}
