import QtQuick 2.14
import QtLocation 5.14
import QtPositioning 5.14

Rectangle{
    height: 500
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

        center:  QtPositioning.coordinate(49.19471,16.60911) // Center to the selected city
        zoomLevel: 14

        MapItemView {
            model: vehiclesModel
            delegate: MapQuickItem {
                coordinate: model.location
                sourceItem: Text{
                    text: model.display
                }
            }
        }
    }
}
