import QtQuick 2.14
import QtQuick.Controls 2.14


Column {
Text {
    text: clickModel.count
}
Button {
    text: 'Click me!'
    onClicked: clickModel.increase()
}
}
