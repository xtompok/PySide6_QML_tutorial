import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQml.Models 2.1
import QtLocation 5.14
import QtPositioning 5.14

Row {
    width: 800
    height: 500

    // Create property holding model of currently selected city
    property var currentModelItem;

    ListView {
        id: cityList
        width: 250
        height: parent.height
        focus: true

        Component {
            id: cityListDelegate
            Item {
                width: parent.width
                height: childrenRect.height
                Text {
                    text: model.display
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: cityList.currentIndex = index
                }
            }
        }

        model: DelegateModel {
            id: cityListDelegateModel
            model: cityListModel
            delegate: cityListDelegate
        }

        // When current item of the list is changed, update the currentModelItem property
        onCurrentItemChanged: currentModelItem = cityListDelegateModel.items.get(cityList.currentIndex).model

        highlight: Rectangle {
            color: "lightsteelblue"
        }
    }

    Column {
        Text {
            text: cityList.currentIndex
        }
        Text {
            text: "Rozloha:"
        }
        Text {
            textFormat: Text.RichText // We need RichText to render upper index correctly
            text: currentModelItem.area+" km<sup>2</sup>"
        }
        Text {
            text: "Počet obyvatel"
        }
        Text {
                text: currentModelItem.population
        }
    }

    Plugin {
        id: mapPlugin
        name: "osm" // We want OpenStreetMap map provider
        PluginParameter {
             name:"osm.mapping.custom.host"
             value:"https://tiles.wmflabs.org/osm-no-labels/" // We want custom tile server for tiles without labels
        }
    }

    Map {
        width: 500
        height: parent.height

        plugin: mapPlugin
        activeMapType: supportedMapTypes[supportedMapTypes.length - 1] // Use our custom tile server

        center: currentModelItem.location // Center to the selected city
        zoomLevel: 10

        MapItemView {
            model: cityListModel
            delegate: MapQuickItem {
                coordinate: model.location
                sourceItem: Text{
                    text: model.display
                }
            }
        }
    }

}
