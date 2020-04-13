import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQml.Models 2.1
import QtLocation 5.14
import QtPositioning 5.14

Row {
    width: 800
    height: 500

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
                height: textid.height
                Text {
                    id: textid
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

        onCurrentItemChanged: currentModelItem = cityListDelegateModel.items.get(cityList.currentIndex).model

        highlight: Rectangle {
            width: parent.width
            height: textid.height
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
            textFormat: Text.RichText
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
        name: "osm" // "mapboxgl", "esri", ...
        PluginParameter {
             name:"osm.mapping.custom.host"
             value:"https://tiles.wmflabs.org/osm-no-labels/"
        }
    }

    Map {
        width: 500
        height: parent.height
        plugin: mapPlugin
        center: currentModelItem.location // Oslo
        zoomLevel: 10
        activeMapType: supportedMapTypes[supportedMapTypes.length - 1]
        MapItemView {
            id: clMapItemView
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
