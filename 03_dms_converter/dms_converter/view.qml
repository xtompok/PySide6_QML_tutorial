import QtQuick 2.14
import QtQuick.Controls 2.14

ApplicationWindow {
    visible: true

    Column {
        id: column
        Row{
            id: row
            spacing: 2
            Label {
                text: 'DMS:'
            }
            TextInput{
                id: degInput
                maximumLength: 3
                width: 20
                text: dmsmodel.deg

                Binding {
                    target: dmsmodel
                    property: "deg"
                    value: degInput.text
                }
            }
            Label{
                text:'° '
            }
            TextInput {
                id: minInput
                text: dmsmodel.min

                Binding {
                    target: dmsmodel
                    property: "min"
                    value: minInput.text
                }
            }
            Label {
                text:'\''
            }
            TextInput {
                id: secInput
                text: dmsmodel.sec

                Binding {
                    target: dmsmodel
                    property: "sec"
                    value: secInput.text
                }
            }
            Label {
                text: '\'\''
            }
            Button {
                onClicked: dmsmodel.to_float()
                text: 'To float'
            }
        }
        Row {
            spacing: 2
            Label {
                text: 'Degrees:'
            }
            TextInput {
                id: degFloatInput
                maximumLength: 10
                width: 30
                text: dmsmodel.deg_float

                Binding {
                    target: dmsmodel
                    property: "deg_float"
                    value: degFloatInput.text
                }

            }
            Button {
                onClicked: dmsmodel.to_dms()
                text: 'To DMS'
            }
        }
        Label{
            text: dmsmodel.deg
        }
    }


}
/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
