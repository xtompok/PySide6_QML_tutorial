import QtQuick 2.14
import QtQuick.Controls 2.14

Column {
    id: column
    Row{
        spacing: 2
        Label {
            text: 'DMS:'
        }
        TextInput{
            id: degInput
            maximumLength: 3
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
            maximumLength: 8
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
}


