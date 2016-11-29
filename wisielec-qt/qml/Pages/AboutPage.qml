import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0

Item {
    property alias renderlabel: renderlabel
    property alias serverlabel: serverlabel
    id: item1
    Rectangle {
        id: rectangle1
        width: 100
        height: 100
        color: "#000"
        radius: 100
        clip: true
        Image {
            anchors.fill: parent
            width: 100
            height: 100
            clip: true
            source: "qrc:/img/avatar.jpg"
        }

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

    Text {
        id: text1
        x: 308
        text: qsTr("renderowane za pomocą:")
        font.bold: true
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: rectangle1.bottom
        anchors.topMargin: 77
        font.pixelSize: 12
    }

    Text {
        id: renderlabel
        x: 301
        y: -8
        text: qsTr("wszystkiego")
        anchors.horizontalCenterOffset: 0
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 12
        anchors.top: rectangle1.bottom
        anchors.topMargin: 93
    }

    Text {
        id: text2
        x: 304
        y: -4
        text: qsTr("adres URL API")
        anchors.horizontalCenterOffset: 0
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 12
        font.bold: true
        anchors.top: rectangle1.bottom
        anchors.topMargin: 118
    }

    Text {
        id: serverlabel
        x: 297
        y: -12
        text: qsTr("127.0.0.1:8000")
        anchors.horizontalCenterOffset: 0
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 12
        anchors.top: rectangle1.bottom
        anchors.topMargin: 138
    }
}
