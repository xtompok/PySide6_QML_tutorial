import QtQuick 2.14
import QtQuick.Controls 2.14

Rectangle {
    width: 200
    height: 500

    ListView {
        anchors.fill: parent
        model: cityListModel

        delegate: Text {
            text: model.display
        }

    }

}