import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0


Item {
    Rectangle {
        id: rectangle1
        width: 100
        height: 100
        color: "#000"
        radius: 100
        anchors {
            top: parent.top
            margins: 40
            horizontalCenter: parent.horizontalCenter
        }
    }
    Label {
        text: "chlebzycia_666"
        font.pointSize: 16
        anchors {
            top: rectangle1.bottom
            margins: 20
            horizontalCenter: rectangle1.horizontalCenter
        }
    }
}
